from random import sample
from MathLib.Vector import Vector2I
from typing import List, Optional
from God import *
from Player import Player


class SettingManager:
    # ~ Video
    screen_size: Vector2I
    # ~ Game Preferences
    players: list[Player] = []
    grid_size: Vector2I
    map_frame_size: Vector2I
    stacks_before_dome: int

    selectable_gods: List[God] = []

    @staticmethod
    def load_defaults() -> None:
        SettingManager.screen_size = Vector2I(1920, 1080)

        SettingManager.grid_size = Vector2I(5, 5)
        SettingManager.map_frame_size = Vector2I(500, 500)

        SettingManager.selectable_gods = [Artemis(), Demeter()]

    @staticmethod
    def assign_gods_random_from_list(selectable_gods: List[God]):
        if len(selectable_gods) < len(SettingManager.players):
            print("Not enough unique gods for all players.")
            return

        rng_selected = sample(
            # ? can also add weights
            selectable_gods, len(SettingManager.players))

        for (p, g) in zip(SettingManager.players, rng_selected):  # assign
            p.assign_god(g)

    @staticmethod
    def initialize_players(count: int):
        SettingManager.players.clear()
        Player.reset_player_count()

        for _ in range(count):
            SettingManager.players.append(Player())
