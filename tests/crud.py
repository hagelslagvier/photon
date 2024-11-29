from inzicht.crud.generic import GenericCRUD
from tests.models import Course, Dummy, Group, Locker, Student


class GroupCRUD(GenericCRUD[Group]):
    pass


class StudentCRUD(GenericCRUD[Student]):
    pass


class CourseCRUD(GenericCRUD[Course]):
    pass


class LockerCRUD(GenericCRUD[Locker]):
    pass


class DummyCRUD(GenericCRUD[Dummy]):
    pass
