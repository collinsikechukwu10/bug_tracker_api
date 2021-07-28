from django.contrib.auth import get_user_model
from django.db import models
import datetime as dt

from django.db.models import Count

from bugTracker.enums import TaskStatus

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    created_on = models.DateField(auto_now_add=True)
    members = models.ManyToManyField(User)
    updated_on = models.DateTimeField(auto_now=True)  # TODO Confirm this
    web_link = models.URLField(max_length=300, null=True)
    google_app_store_link = models.URLField(max_length=300, null=True)
    apple_app_store_link = models.URLField(max_length=300, null=True)

    def last_updated(self):
        return int((dt.datetime.now(self.updated_on.tzinfo) - self.updated_on).seconds / (60*60))

    def get_task_count(self):
        status_dict = list(self.tasks.values("status").annotate(count=Count("status")))
        status_count_dict = {i["status"]: i["count"] for i in status_dict}
        for i in TaskStatus.values():
            if i not in status_count_dict:
                status_count_dict[i] = 0
        return status_count_dict


class ProjectSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE),
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    email_notification = models.BooleanField(default=False)
