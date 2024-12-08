from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    LEADERBOARD = auto()
    GAME_OVER = auto()
    PAUSE = auto()
