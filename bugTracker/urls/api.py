from django.urls import path
from bugTracker.views import api as views

#
_name_appender = lambda i: f"api_bugtracker{i}"
urlpatterns = [
    path("projects/<int:pk>/tasks", views.project_task_list, name=_name_appender("projecttasklist")),
    path("projects/<int:pk>/metrics", views.project_metrics, name=_name_appender("projecttaskmetrics")),
    path("task/update-status", views.update_task_status, name=_name_appender("updatetaskstatus")),
    path("projects", views.project_list, name=_name_appender("projectlist")),
    path("projects/<int:pk>", views.project_detail, name=_name_appender("projectdetail")),
    path("projects/<int:pk>/export", views.export_project, name=_name_appender("exportproject"))
]
