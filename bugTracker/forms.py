from django import forms

from bugTracker.models.service import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["updated_on", "fixed_on", "fix_verified_on", "created_on", "reporter"]
