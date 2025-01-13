from enum import Enum, auto


class PlayerStatus(Enum):
    NORMAL = auto()
    GROWING = auto()
    BIG = auto()
    DYING = auto()
    GAME_OVER = auto()

class NokonokoStatus(Enum):
    NORMAL = auto()
    SHELL = auto()
    SHELL_MOVING = auto()
