from enum import Enum


class MembershipDescription:
    def __init__(self, name: str, level: int):
        self._name = name
        self._level = level

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._name.lower()

    @property
    def level(self):
        return self._level

    def __str__(self):
        return self.display_name


class DefaultMembershipEnum(Enum):
    UNASSIGNED = MembershipDescription("UNASSIGNED", 0)
    DEVELOPER = MembershipDescription("DEVELOPER", 2)
    GUEST = MembershipDescription("GUEST", 1)
    TESTER = MembershipDescription("TESTER", 3)

    @classmethod
    def resolve_membership(cls, value):
        pass
# TODO IMPLEMENT
