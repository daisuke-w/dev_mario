from enum import Enum, auto


class Status(Enum):
    NORMAL = auto()
    DYING = auto()
    GAME_OVER = auto()
