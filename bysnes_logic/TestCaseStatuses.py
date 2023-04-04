import enum

@enum.unique
class TestCaseStatuses(enum.IntEnum):
    passed = 1
    failed = 2
    not_executed = 3