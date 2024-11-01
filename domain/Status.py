import enum


class Status(enum.Enum):
    COMPLETED = 1
    RUNNING = 2
    STOPPED = 3
    ERROR = 4
    UNKNOWN = 5
