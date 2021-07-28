from django.urls import path
from core.views import api as views

_name_appender = lambda i: f"api_core_{i}"

urlpatterns = [
    path("adduser", views.create_new_user, name=_name_appender("create_user")),
    path("deleteuser/<int:pk>", views.delete_user, name=_name_appender("delete_user"))
]
