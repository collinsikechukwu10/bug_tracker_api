from django.contrib.auth import get_user_model
from core.models import Membership
from core.enums import DefaultMembershipEnum

User = get_user_model()


def initialize():
    initialize_membership_roles()
    initialize_users()


def initialize_users():
    users = User.objects.filter(is_staff=False, is_superuser=False)
    if len(users) == 0:
        membership = Membership.objects.get(name=str(DefaultMembershipEnum.UNASSIGNED.value))
        if membership:
            new_user = User.objects.create_user(username="ubuntu@sankore.com", email="ubuntu@sankore.com",
                                                password="password", membership=membership)
            new_user.save()


def initialize_membership_roles():
    if Membership.objects.count() == 0:
        for enum in DefaultMembershipEnum.__members__.values():
            membership = Membership(name=str(enum.value), level=enum.value.level)
            membership.save()
