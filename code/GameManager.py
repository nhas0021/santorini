from GameLogic import Game
from typing import Optional
from SettingManager import SettingManager

#used to form connection between the actual game and UI elements, A singleton.
class GameManager():
    current_game: Optional[Game] = None

    @staticmethod
    def setup_game():
        GameManager.current_game = Game(SettingManager.player_count, SettingManager.grid_size)

    @staticmethod
    def get_game() -> Game:
        return GameManager.current_game
        
