from enum import Enum, auto

class GameState(Enum):
    NOT_RUNNING = auto()
    TITLE_SCREEN = auto()
    LEVEL_SELECT = auto()
    IN_LEVEL = auto()
    GAME_OVER = auto()
