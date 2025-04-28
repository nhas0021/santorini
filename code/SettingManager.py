from random import sample
from MathLib.Vector import Vector2I
from typing import List, Optional
from God import *

#allows to change the settings later
class SettingManager:
    # ~ Video
    screen_size: Vector2I
    # ~ Game Preferences
    #players: list[Player] = []
    grid_size: Vector2I
    map_frame_size: Vector2I
    max_stacks_before_dome: int
    selectable_gods: List[God] = []
    player_count: int

    @staticmethod
    def load_defaults() -> None:
        SettingManager.screen_size = Vector2I(1920, 1080)

        SettingManager.grid_size = Vector2I(5, 5)
        SettingManager.map_frame_size = Vector2I(500, 500)

        SettingManager.selectable_gods = [Artemis(), Demeter()]
        SettingManager.player_count = 2
        SettingManager.max_stacks_before_dome = 3
