from io import BytesIO
import pandas as pd
from django.db import models
from django.db.models import Count

from bugTracker.enums import TaskStatus
from bugTracker.models.project import Project
from bugTracker.models.task import Task, TaskTrail, TaskMetrics, TaskUpdateMixin
from bugTracker.models.serializers import SerializerFactory
import datetime as dt


class ServiceMixin:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


class ModelServiceMixin(ServiceMixin):
    _serializer = None

    @property
    def has_serializer(self):
        return self._serializer is not None


class ProjectService(ModelServiceMixin):
    def __init__(self):
        self._model = Project
        self._serializer = SerializerFactory.get_serializer(Project)

    def find_recent_projects(self, num: int, serialize: bool = True):
        num_projects = self._model.objects.count()
        projects = self._model.objects.order_by("-created_on")[:min(num_projects, num)]
        return self._serializer(projects, many=True).data if (serialize and self.has_serializer) else projects

    def get_project_members(self, pk):
        return self.get_project(pk, False).get_project_members()

    def get_all_projects(self, serialize: bool = True):
        projects = self._model.objects.all().order_by("-created_on")
        return self._serializer(projects, many=True).data if (serialize and self.has_serializer) else projects

    def get_project(self, project_id: int, serialize: bool = True):
        try:
            obj = self._model.objects.get(pk=project_id)
        except self._model.DoesNotExist:
            obj = None
        if obj is None:
            return None
        return self._serializer(obj).data if (serialize and self.has_serializer) else obj

    def order_tasks_by_status(self, project_id):
        task_serializer = SerializerFactory.get_serializer(Task)
        status_values = TaskStatus.values()
        try:
            project = self._model.objects.get(pk=project_id)
        except:
            return {k: [] for k in status_values}
        return_dict = {}
        tasks = project.tasks
        for status in status_values:
            tasks = tasks.filter(status=status)
            return_dict[status] = task_serializer(tasks, many=True).data
        return return_dict


class TaskTrailService(ModelServiceMixin):
    def __init__(self):
        self._model = TaskTrail
        self._serializer = SerializerFactory.get_serializer(self._model)

    def get_task_history(self, task_id, serialize=True):
        trails = TaskTrail.objects.filter(task_id=task_id).order_by("-updated_on")
        return self._serializer(trails, many=True).data if (serialize and self.has_serializer) else trails

    def get_project_task_history(self, project_id, serialize=True):
        trails = TaskTrail.objects.filter(task__project_id=project_id).order_by("-updated_on")
        return self._serializer(trails, many=True).data if (serialize and self.has_serializer) else trails


class TaskService(TaskUpdateMixin, ModelServiceMixin):
    def __init__(self):
        self._model = Task
        self._serializer = SerializerFactory.get_serializer(Task)

    def get_project_tasks(self, project_id, start_date: dt.date = None, end_date: dt.date = None,
                          all_tasks: bool = True,
                          serialize: bool = True):
        end_date = dt.date.today() if end_date is None else end_date
        start_date = dt.date.today() - dt.timedelta(weeks=52) if start_date is None else start_date
        if start_date > end_date:
            raise Exception("Start date cannot be more than end date")
            # find project
        filter_ = dict(project_id=project_id)
        if not all_tasks:
            filter_.update(dict(created_on__gte=start_date, created_on__lte=end_date))
        tasks = self._model.objects.filter(**filter_).order_by("created_on")
        return self._serializer(tasks, many=True).data if (serialize and self.has_serializer) else tasks

    def get_project_task_metrics(self, project_id, start_date: dt.date = None, end_date: dt.date = None,
                                 all_tasks: bool = True,
                                 serialize: bool = True):
        tasks = self.get_project_tasks(project_id, start_date, end_date, all_tasks, serialize=False)
        metrics = TaskMetrics(tasks)
        return metrics.as_json() if serialize else metrics.as_dict()

    def perform_task_status_update(self, user, task_id, status) -> bool:
        try:
            task = self._model.objects.get(pk=task_id)
            status_enum = TaskStatus.find(status)
            handler = self.get_task_update_handler(status_enum)
            handler(task)
            TaskTrail.create_trail(task, status_enum, user)
            return True
        except Exception as e:
            # TODO log exception
            return False

    def delete_task(self, task_id):
        pass


class ExporterService(ServiceMixin):
    def __init__(self):
        self._task_service = TaskService()
        self._project_service = ProjectService()

    @staticmethod
    def parse_model(queryset) -> pd.DataFrame:
        if isinstance(queryset, models.manager.QuerySet):
            data = list(queryset.values())
        else:
            data = queryset
        queryset_dataframe = pd.DataFrame(data)
        print(queryset_dataframe.head())
        return queryset_dataframe

    # @staticmethod
    # def export_queryset_as_csv(response: HttpResponse, queryset: models.manager.QuerySet):
    #     response['Content-Type'] = 'text/csv'
    #     response['Content-Disposition'] = f'attachment; filename={model_name}_{dt.datetime.utcnow().isoformat()}.csv'

    def export_project_as_excel_file(self, pk) -> BytesIO:
        tasks = self._task_service.get_project_tasks(pk, serialize=False)
        tasks_df = self.parse_model(tasks)
        for col in tasks_df.select_dtypes(include=['datetime64[ns]', pd.DatetimeTZDtype]).columns:
            tasks_df[col] = tasks_df[col].dt.tz_localize(None)

        metrics = self._task_service.get_project_task_metrics(pk, serialize=False)
        metrics_df = self.parse_model(metrics)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter', options={'remove_timezone': True}) as writer:
            # write title
            metrics_end_point = len(metrics_df)
            metrics_df.to_excel(writer, sheet_name="tasks", index=False)
            tasks_df.to_excel(writer, startrow=metrics_end_point + 5, sheet_name="tasks", index_label="S/N",
                              header=True)
        output.seek(0)
        return output

    @staticmethod
    def generate_excel_file_name(model_class: models.Model = Project):
        return f"{model_class}_{dt.datetime.utcnow().isoformat()}.xlsx"
