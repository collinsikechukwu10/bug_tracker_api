from enum import Enum


class UserDefinedPermissionTypes(Enum):
    View = "view"
    Update = "update"
    Delete = "delete"


class SuperUserPermissions(Enum):
    ASSIGN_PERMISSION = "assign_user_permission"
    VIEW_ALL_USER_PERMISSION = "view_all_user_permission"
    ALL = "all"
    CREATE_NEW_USER = "create_user"


class PermissionService:
    #
    # def grant_permissions(self, request):
    #     permissions = request.POST.get("permissions",None)
    #     if permissions is not None:
    #         usr = request.user
    #         user.permissions.
    def get_permission_name(self, model, permission: UserDefinedPermissionTypes):
        return f"{permission.value}_{model.__name__.lower()}"
