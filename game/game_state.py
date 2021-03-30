from enum import Enum, auto

class GameState(Enum):
    NOT_RUNNING = auto()
    IN_LEVEL = auto()
    GAME_OVER = auto()
