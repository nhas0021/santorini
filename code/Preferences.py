from __future__ import annotations

from God import *
from MathLib.Vector import Vector2I
from typing import List, Optional, Type


class Preferences:
    """
    Contains settings and preferences about the game. Some may be exposed or user controlled, others may be only developer accessable (or launch args)
    """
    # ! Note: currently it does not load settings from file but can be made to do so if needed
    # ~ Video
    screen_size: Vector2I
    # ~ Game Preferences
    grid_size: Vector2I
    map_frame_size_px: Vector2I
    max_stacks_before_dome: int

    gods_selectable: List[Type[God]] = []

    player_count: int
    gods_preferences: List[Optional[Type[God]]] = []
    reassign_gods_during_game: bool = False

    @staticmethod
    def load_defaults() -> None:
        Preferences.screen_size = Vector2I(1920, 1080)

        Preferences.grid_size = Vector2I(5, 5)
        Preferences.map_frame_size_px = Vector2I(500, 500)

        Preferences.gods_selectable = [Artemis, Demeter, Zeus]
        Preferences.player_count = 2
        Preferences.max_stacks_before_dome = 3
