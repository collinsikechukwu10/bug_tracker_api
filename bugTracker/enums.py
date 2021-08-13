from enum import Enum


class DjangoDbChoicesEnum(Enum):

    @classmethod
    def class_name(cls):
        return cls.__class__.__name__

    @classmethod
    def choices(cls):
        return [(enum_.name, enum_.value) for enum_ in cls.__members__.values()]

    @classmethod
    def find(cls, value):
        enum_dict = {enum_.value: enum_ for enum_ in cls.__members__.values()}
        return enum_dict.get(value, None)

    @classmethod
    def values(cls):
        return [enum_.value for enum_ in cls.__members__.values()]


class Roles(DjangoDbChoicesEnum):
    SUPER_ADMIN = "SUPER_ADMIN"


class TaskStatus(str, DjangoDbChoicesEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    DONE = "done"


class TaskType(str, DjangoDbChoicesEnum):
    BUG = "bug"
    IMPROVEMENT = "improvement"
    RECOMMENDATION = "recommendation"
    FUTURE_UPDATE = "future_update"


class SeverityLevel(str, DjangoDbChoicesEnum):
    CRITICAL = "critical"
    IMPORTANT = 'important'
    MINOR = 'minor'
    NORMAL = 'normal'


class UserPlatform(str, DjangoDbChoicesEnum):
    WEB = 'web'
    MOBILE = "mobile"
    DESKTOP = "desktop"
    NONE_TYPE = "none"


class PriorityLevel(str, DjangoDbChoicesEnum):
    HIGH = "high"
    NORMAL = "normal"
    VERY_HIGH = "very_high"


class Status(str, DjangoDbChoicesEnum):
    NOT_STARTED = "not-started"
    FIXED = "fixed"
    STARTED = "started"
    UNDER_REVIEW = "reviewing"
