from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import *
from django.db import transaction
from django.http.response import StreamingHttpResponse
import datetime as dt

from bugTracker.enums import TaskStatus
from bugTracker.models.service import ProjectService, TaskService, TaskTrailService, ExporterService


@require_GET
@login_required()
def project_dashboard(request):
    projects = ProjectService.get_instance().get_all_projects(False)
    return render(request, "bug_tracker/dashboard.html", {"projects": projects})


@require_GET
@login_required()
def project_tasks_dashboard(request, pk: int):
    project_service = ProjectService.get_instance()
    project = project_service.get_project(pk, serialize=False)
    statuses = TaskStatus.values()
    status_dict = project_service.order_tasks_by_status(project.id)
    request.session.setdefault("project_id", pk)
    return render(request, "bug_tracker/tasks/index.html",
                  {"project_id": pk})

#
# @require_POST
# @login_required()
# def create_project(request):
#     project_form = ProjectForm(request.POST)
#     # usr = request.user
#     if project_form.is_valid() and not project_form.errors:
#         project_form.save_m2m()
#         if request.is_ajax():
#             return JsonResponse(
#                 BaseResponse.get_success_response(data=dict(project=project_form.instance.values())).dict(),
#                 status=200)
#         else:
#             return redirect(project_form.instance)
#     else:
#         if request.is_ajax():
#             return JsonResponse(
#                 BaseResponse.get_failed_response("Could not create project,
#                 data sent is not valid").dict(), status=200)
#         else:
#             projects = ProjectService.get_all_projects()
#             return render(request, "bug_tracker/dashboard.html", dict(form=project_form, projects=projects))
#
#
# @require_GET
# @login_required()
# def tasks_list(request):
#     tasks = TaskService.get_all_tasks()
#     if request.is_ajax():
#         return JsonResponse(BaseResponse.get_success_response(data=dict(tasks=tasks.values())).dict(), status=200)
#     else:
#         task_form = TaskForm()
#         return render(request, "bug_tracker/index.html", dict(tasks=tasks, form=task_form))
#
#
# @require_POST
# @login_required()
# @transaction.atomic()
# def create_task(request):
#     files = request.FILES or None
#     task_form = TaskForm(request.POST, files)
#     usr = request.user
#     task_form.reporter = usr
#     if task_form.is_valid() and not task_form.errors:
#         TaskService.get_task_update_handler(TaskStatus.OPEN)(task_form.instance, usr)
#         task_form.save_m2m()
#         if request.is_ajax():
#             return JsonResponse(BaseResponse.get_success_response(data=dict(task=task_form.instance.values())).dict(),
#                                 status=200)
#         else:
#             return redirect(task_form.instance)
#     else:
#         if request.is_ajax():
#             return JsonResponse(
#                 BaseResponse.get_failed_response("Could not create task, data sent is not valid").dict(), status=200)
#         else:
#             form = TaskForm(initial=task_form.data)
#             return render(request, "bug_tracker/index.html", {'form': form})
#
#
# @require_GET
# @login_required()
# def project_detail(request, pk: int):
#     obj = get_object_or_404(Project, **{"pk": pk})
#     # get tasks for project
#     tasks = obj.tasks.all()
#     if request.is_ajax():
#         return JsonResponse(BaseResponse.get_success_response(data=dict(project=obj,
#         tasks=tasks.values())), status=200)
#     else:
#         return render(request, "bug_tracker/detail/project_detail.html", dict(project=obj, tasks=tasks))
#
#
