from enum import Enum


class DjangoDbChoicesEnum(Enum):
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
    OPEN = "opened"
    IN_PROGRESS = "progress"
    TESTING = "testing"
    DONE = "done"


class TaskType(str, DjangoDbChoicesEnum):
    BUG = "bug"
    IMPROVEMENT = "improvement"
    RECOMMENDATION = "recommendation"
    FUTURE_UPDATE = "future_update"


class SeverityLevel(str, DjangoDbChoicesEnum):
    CRITICAL = "critical"
    MAJOR = 'major'
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


class PreDefinedTeams(str, DjangoDbChoicesEnum):
    AITEAM = "ai-team"
    DEVELOPERS = "developers"
    LEGAL = "legal-team"
    FUNDS = "funds-team"
    QATEAM = "qa-team"
    LOIS = "lois"
    DAMILOLA = 'damilola'
    NONE_TYPE = None


class PreDefinedCompanies(str, DjangoDbChoicesEnum):
    WEALTHTECH = "wealth-tech"
    SANKORE = "sankore"


class Reporter(str, DjangoDbChoicesEnum):
    DEFAULT = "default-reporter"
