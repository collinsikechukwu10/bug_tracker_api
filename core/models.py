from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer
from core.enums import DefaultMembershipEnum


class Membership(models.Model):
    name = models.CharField(max_length=100)
    level = models.SmallIntegerField()

    class Meta:
        unique_together = ("name", "level",)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False)
    image = models.URLField(null=True)
    membership = models.ForeignKey(Membership, on_delete=models.PROTECT)

    def get_initials(self):
        return self.first_name[0] + self.last_name[0]

    @classmethod
    def get_users(cls):
        # only show non superusers,
        return cls.objects.filter(is_superuser=False)


class UserSerializer(ModelSerializer):
    class Meta:
        exclude = ("password", "")
        model = CustomUser


# class UserSettings(models.Model):
#     pass
#

class UserService:

    @staticmethod
    def get_all_email_addresses():
        return CustomUser.objects.values_list("email", flat=True)
