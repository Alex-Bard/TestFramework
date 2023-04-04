import enum

@enum.unique
class TestCasLogStatuses(enum.IntEnum):
    warning = 1
    success = 2
    danger = 3
    info = 4