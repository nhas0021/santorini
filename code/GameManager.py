from Game import Game
from typing import Optional
from God import *

#used to form connection between the actual game and UI elements, A singleton.
class GameManager:
    current_game: Optional[Game] = None
    gods = [Artemis(), Demeter()] #for testing purpose, do we wanna keep it here?

    @staticmethod
    def setup_game(player_count, grid_size):
        GameManager.current_game = Game(player_count, grid_size, GameManager.gods)

    @staticmethod
    def get_game() -> Game:
        return GameManager.current_game