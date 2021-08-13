from django.http.response import StreamingHttpResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as status_util
import datetime as dt
from bugTracker.enums import Roles, TaskType, TaskStatus, SeverityLevel, UserPlatform, PriorityLevel, Status
##########################
# API VIEW HANDLERS      #
##########################
from bugTracker.models.service import ProjectService, TaskService, ExporterService
from bugTracker.utilities import BaseResponse


@api_view(["GET"])
def project_list(request: Request):
    projects = ProjectService.get_instance().get_all_projects()
    return Response(data=BaseResponse.get_success_response(None, projects), status=status_util.HTTP_200_OK)


def get_dates_dict_from_request(request: Request, params):
    for optional_date in ["start_date", "end_date"]:
        date = request.query_params.get(optional_date, None)
        if date is not None:
            try:
                parsed_ = dt.date.strftime(date, "%d-%m-%Y")
                params[optional_date] = parsed_
            except:
                continue


@api_view(["GET"])
def data_enum_list(request: Request):
    data_list = {}
    for i in [Roles, TaskType, TaskStatus, SeverityLevel, UserPlatform, PriorityLevel, Status]:
        data_list[i.__name__] = i.values()
    return Response(data=BaseResponse.get_success_response(None, data_list), status=status_util.HTTP_200_OK)


@api_view(["GET"])
def project_detail(request: Request, pk: int):
    tasks = TaskService.get_instance().get_project_tasks(pk)
    members = ProjectService.get_instance().get_project_members(pk)
    response_data = dict(tasks=tasks, members=members)
    return Response(data=BaseResponse.get_success_response(None, response_data), status=status_util.HTTP_200_OK)


@api_view(["GET"])
def project_task_list(request: Request, pk: int):
    filter_ = dict(project_id=pk)
    sort_by = request.query_params.get("by", None)
    if sort_by == "status":
        result_dict = ProjectService.get_instance().order_tasks_by_status(**filter_)
    else:
        get_dates_dict_from_request(request, filter_)
        if len(filter_) > 1:
            filter_["all_tasks"] = False
        result_dict = TaskService.get_instance().get_project_tasks(**filter_)
    return Response(data=BaseResponse.get_success_response(None, result_dict), status=status_util.HTTP_200_OK)


@api_view(["GET"])
def project_metrics(request: Request, pk: int):
    filter_ = dict(project_id=pk)
    get_dates_dict_from_request(request, filter_)
    if len(filter_) > 1:
        filter_["all_tasks"] = False
    filter_["serialize"] = False
    metrics = TaskService.get_instance().get_project_task_metrics(**filter_)
    return Response(data=metrics, status=status_util.HTTP_200_OK)


@api_view(["GET"])
def export_project(request, pk: int):
    bytes_io_data = ExporterService.get_instance().export_project_as_excel_file(pk)
    response = StreamingHttpResponse(bytes_io_data)
    response['Content-Type'] = 'text/csv'
    response[
        'Content-Disposition'] = f'attachment; filename={ExporterService.get_instance().generate_excel_file_name()}'
    return response


# @api_view(["GET"])
# def project_detail(request: Request, pk: int):
#     project = ProjectService.get_instance().get_project(project_id=pk)
#     project = project if project is not None else dict()
#     return Response(project, status_util.HTTP_200_OK)


@api_view(["POST"])
def update_task_status(request: Request):
    user_ = request.user
    data = request.data
    kwargs = {}
    for key in ["status", "task_id"]:
        val_ = data.get(key, None)
        if val_ is None:
            return Response(data=f"Missing {key} in data", status=status_util.HTTP_400_BAD_REQUEST)
        kwargs[key] = val_
    kwargs.update(dict(user=user_))
    status, response_message = TaskService.perform_task_status_update(**kwargs)
    return Response(BaseResponse.get_success_response(response_message) if status else BaseResponse.get_failed_response(
        response_message), status_util.HTTP_200_OK)
