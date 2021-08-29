from enum import Enum

class Level(int, Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    @staticmethod
    def from_string(string: str) -> 'Level':
        string = string.lower()

        if string in ("critical", "FATAL"):
            return Level.CRITICAL
        elif string in ("warn", "warning"):
            return Level.WARNING
        elif string == "info":
            return Level.INFO
        elif string == "debug":
            return Level.DEBUG
        else:
            return Level.NOTSET