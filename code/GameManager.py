from GameState import MapState
from typing import List, Optional, Type, cast
from God import God
from Preferences import Preferences

# used to form connection between the actual game and UI elements, A singleton.


class GameManager():
    _current_game: Optional[MapState] = None

    @staticmethod
    def setup_game():

        GameManager._current_game = MapState(
            Preferences.player_count, cast(List[Type[God]], Preferences.gods_preferences), Preferences.grid_size, Preferences.max_stacks_before_dome)

    @staticmethod
    def get_game():
        assert GameManager._current_game
        return GameManager._current_game
