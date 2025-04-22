import tkinter as tk
from MathLib.Vector import Vector2I
from SceneID import SceneID
from Styles import *
from God import God

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


class GameScene(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)


class MatchData:
    """
    Stores all the information for a game/match.
    Implementation hides away the actual storage method/s.

    Note for hexagonal:
        - https://www.redblobgames.com/grids/hexagons/#map-storage
            - Python does not have 2D arrays - ONLY OPTIONS: Array of Arrays or Hash Table
    """

    def __init__(self, player_count: int, size: Vector2I):
        self._grid: list[list[Tile]] = [
            [Tile(Vector2I(x, y)) for x in range(size.y)] for y in range(size.x)]
        
        self.players: list[Player] = [] * player_count

    def get_tile(self, position: Vector2I):
        return self._grid[position.x][position.y]

class Player:
    def __init__(self):
        self.god:God


class Tile:
    def __init__(self, position: Vector2I):
        self.position: Vector2I = position  # ? Might not need
        self.stack_height: int = 0
