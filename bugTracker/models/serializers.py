from typing import Type

from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedRelatedField
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from bugTracker.models.project import Project
from bugTracker.models.task import Task, TaskTrail
from core.models import UserSerializer


def register_serializer(model_class):
    def wrapper_register_serializer(func):
        SerializerFactory.add_serializer(model_class, func)

    return wrapper_register_serializer


class SerializerFactory:
    _serializer_classes = {}

    @staticmethod
    def get_serializer(model_class) -> Type[ModelSerializer]:
        return SerializerFactory._serializer_classes.get(model_class, None)

    @staticmethod
    def add_serializer(model_class, serializer):
        if model_class not in SerializerFactory._serializer_classes.keys():
            SerializerFactory._serializer_classes[model_class] = serializer

api_name_appender = lambda i: f"api_bugtracker{i}"

@register_serializer(Project)
class ProjectSerializer(ModelSerializer):
    task_url = HyperlinkedRelatedField(
        view_name="api_bugtrackerprojecttasklist",
        read_only=True,
        lookup_field='pk'
    )
    task_count = SerializerMethodField()
    last_updated_hours = SerializerMethodField()

    def get_task_count(self, obj):
        return obj.get_task_count()

    def get_last_updated_hours(self, obj):
        return obj.last_updated()

    class Meta:
        model = Project
        fields = "__all__"
        depth = 3


@register_serializer(Task)
class TaskSerializer(TaggitSerializer, ModelSerializer):
    tags = TagListSerializerField()
    checklists = SerializerMethodField()
    by = SerializerMethodField()

    def get_by(self, obj):
        return obj.reporter.get_full_name()

    def get_checklists(self, obj):
        return obj.decode_checklists()

    class Meta:
        model = Task
        fields = "__all__"


@register_serializer(TaskTrail)
class TaskTrailSerializer(ModelSerializer):
    class Meta:
        model = TaskTrail
        fields = "__all__"

# @register_serializer(Tag)
# class TagSerializer(ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = "__all__"
