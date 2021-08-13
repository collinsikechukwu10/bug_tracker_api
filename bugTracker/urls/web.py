from django.urls import path
from bugTracker.views import web as views

#
_name_appender = lambda i: f"bugtracker_{i}"
urlpatterns = [
    path("dashboard", views.project_dashboard, name=_name_appender("projectdashboard")),
    path("projects/<int:pk>", views.project_tasks_dashboard, name=_name_appender("projecttaskdashboard"))
]
