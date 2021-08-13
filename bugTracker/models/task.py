import json
from typing import List, Dict, Any

from django.db import models
from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import Cast
from taggit.managers import TaggableManager

from .project import Project
from ..enums import *
import datetime as dt
from django.contrib.auth import get_user_model

from ..utilities import send_notification_email

User = get_user_model()

STEPS_APPENDER = "%%NEWSET%%"
ID_TEXT_SPLIT = "%%AND%%"
checklist_formatter = lambda key, text: f"{key}{ID_TEXT_SPLIT}{text}{STEPS_APPENDER}"


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name="tasks", null=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="reported_tasks",
                                 default=None, blank=True, null=True)
    task_type = models.CharField(choices=TaskType.choices(), max_length=20, default=TaskType.BUG)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=TaskStatus.choices(), max_length=15, default=TaskStatus.OPEN)
    severity = models.CharField(choices=SeverityLevel.choices(), max_length=15, default=SeverityLevel.NORMAL)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name="assigned_tasks")
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(default="")
    image = models.ImageField(upload_to="task_media/screenshot")
    video = models.FileField(upload_to="task_media/video")
    fixed_on = models.DateTimeField(null=True)
    due_date = models.DateField(null=True)
    # fix_verified_on = models.DateTimeField(null=True)
    updated_on = models.DateTimeField(auto_now=True)
    checklists = models.TextField(blank=True, default="")
    tags = TaggableManager()

    def is_overdue(self):
        if self.due_date is not None:
            return self.due_date <= dt.date.today()
        return False

    def encode_checklists(self, steps: List[Dict[str, Any]]):
        # this list has to be ordered
        return "".join(map(checklist_formatter, steps))

    def decode_checklists(self):
        steps = self.checklists.split(STEPS_APPENDER)
        if len(steps) == 0:
            return []
        decoded = []
        for step in filter(lambda i: i.strip() != "", steps):
            id_, text = step.split(ID_TEXT_SPLIT)
            decoded.append(dict(id=id_, text=text))
        return decoded

    @property
    def can_complete(self):
        return self.status == TaskStatus.IN_PROGRESS

    @property
    def can_reopen(self):
        return self.status != TaskStatus.OPEN

    @property
    def can_set_to_in_progress(self):
        return self.status != TaskStatus.IN_PROGRESS


class TaskTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="task_trails")
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name="trails")
    updated_on = models.DateTimeField(auto_now_add=True)
    task_status = models.CharField(choices=TaskStatus.choices(), max_length=15, default=TaskStatus.OPEN)

    @classmethod
    def create_trail(cls, task: Task, status: TaskStatus, user: User):
        if task.status == status and status != TaskStatus.UPDATED:
            raise Exception("You are trying to duplicate a status")
        obj = cls(user=user, task=task, task_status=status)
        obj.save()


# class Tag(models.Model):
#     value = models.CharField(max_length=100, unique=True)
#     count = models.BigIntegerField()
#
#     @classmethod
#     def search(self):
#         pass


class TaskMetrics:
    def __init__(self, tasks):
        self._tasks = tasks
        self._data = None
        self._analyze_tasks()

    def _analyze_tasks(self):
        total_tasks_count = self._tasks.count()
        status_count = self._tasks.values("status").annotate(count=Count("status"),
                                                             percentage=Cast(Count('status'),
                                                                             models.FloatField()) / total_tasks_count
                                                             ).order_by("status")
        severity_count = self._tasks.values("severity").annotate(count=Count("severity"),
                                                                 percentage=Cast(Count('severity'),
                                                                                 models.FloatField()) / total_tasks_count
                                                                 ).order_by("severity")
        self._data = dict(status_summary=list(status_count), severity_summary=list(severity_count))

    def as_dict(self):
        return self._data

    def as_json(self):
        return json.dumps(self._data)


class TaskUpdateMixin:
    def _reopen_task(self, task: Task):
        if task.can_reopen:
            task.status = TaskStatus.OPEN
            task.fixed_on = None
            task.fix_verified_on = None
            task.save()
        else:
            raise Exception("Only fixes that have been verified can be reopen")

    def _complete_task(self, task: Task):
        if task.can_complete:
            task.status = TaskStatus.COMPLETE
            task.fixed_on = dt.datetime.now()
            # task.fix_verified_on = None
            task.save()
        else:
            raise Exception("Only opened or reopened tasks can be submitted as fixed")

    def _progress_task(self, task: Task):
        if task.can_set_to_in_progress:
            task.status = TaskStatus.IN_PROGRESS
        task.save()

    def _create_task(self, task: Task):
        task.save()

    def _default_update_task(self, task: Task):
        task.save()

    def get_task_update_handler(self, required_status: TaskStatus):
        return {
            TaskStatus.OPEN: self._create_task,
            TaskStatus.IN_PROGRESS: self._progress_task,
            TaskStatus.COMPLETE: self._complete_task
        }.get(required_status, self._default_update_task)
