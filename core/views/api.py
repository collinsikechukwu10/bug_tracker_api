from django.contrib.auth.decorators import user_passes_test, login_required
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status as status_util
from core.forms import RegisterForm
from core.utils import SuperUserPermissions
from core.models import CustomUser, UserSerializer


def can_handle_user_permissions(user):
    return True if user.has_perms(
        [SuperUserPermissions.ASSIGN_PERMISSION, SuperUserPermissions.VIEW_ALL_USER_PERMISSION]) or user.has_perms(
        SuperUserPermissions.ALL) else False


def is_super_user(user):
    return user.is_superuser


def can_create_new_users(user):
    return True if user.has_perms(SuperUserPermissions.CREATE_NEW_USER) or user.has_perms(
        SuperUserPermissions.ALL) else False


@api_view(["POST"])
@login_required()
@user_passes_test(is_super_user)
def create_new_user(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        obj_usr = form.instance
        instance = obj_usr.save()
        return Response(data=UserSerializer(instance).data, status=status_util.HTTP_201_CREATED)

    else:
        return Response(data=form.errors, status=status_util.HTTP_200_OK)


@api_view(["POST"])
@login_required()
@user_passes_test(is_super_user)
def delete_user(request: Request, pk: int):
    try:
        obj = CustomUser.objects.get(pk=pk)
        obj.delete()
        return Response(data="User deleted successfully", status=status_util.HTTP_201_CREATED)
    except Exception as e:
        if isinstance(e, CustomUser.DoesNotExist):
            return Response("User does not exist", status=status_util.HTTP_202_ACCEPTED)
        else:
            return Response("Error occurred when deleting user", status=status_util.HTTP_500_INTERNAL_SERVER_ERROR)
