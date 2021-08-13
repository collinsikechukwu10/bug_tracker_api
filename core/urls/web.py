from django.urls import path
from core.views import web as views

_name_appender = lambda i: f"core_{i}"

urlpatterns = [
    path("", views.home, name=_name_appender("login")),
    path("login", views.auth_login, name=_name_appender("login")),
    path("logout", views.auth_logout, name=_name_appender("logout")),
    path("users", views.users_page, name=_name_appender("users_page")),
    path("register", views.register, name=_name_appender("register"))
    # path("user_permissions_factory", views.permissions_factory, name=_name_appender("perms_factory")),
    # path("update_permissions", views.permissions_factory, name=_name_appender("perms_update"))
]
