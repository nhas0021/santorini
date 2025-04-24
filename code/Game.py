from dataclasses import dataclass
from tkinter import Canvas, Tk, Button, Frame
from typing import Callable, Optional
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
from Styles import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


@dataclass
class Tile:
    """
    Defaults are what a tile is before anything happens on them. 
    """
    # ! Gameplay Data
    position: Vector2I
    stack_height: int = 0
    worker: int = 0
    # ! Interaction Data
    on_click_callback: Optional[Callable] = None


class Player:
    def __init__(self):
        self.hero_id: int


# class MapRenderer:
#     def __init__(self, match_data: MatchData, render_size: Vector2I):
#         self.render_frame = Frame(
#             None, width=render_size.x, height=render_size.y, background=DEBUG_ERR_COLOUR, border=1)

#         # self._grid: list[list[Button]] = [
#         #     [Button(self.render_frame, text=f"{x}-{y}") for x in range(match_data.size.y)] for y in range(match_data.size.x)]


#     def get_tile(self, position: Vector2I):
#         return self._grid[position.x][position.y]

class GameScene(Scene):
    def __init__(self, root: Tk, map_render_size: Vector2I) -> None:
        super().__init__(root)

        self.size: Optional[Vector2I] = None
        self._grid: Optional[list[list[Tile]]] = None
        self.map_frame: Frame = Frame(
            self.frame, width=map_render_size.x, height=map_render_size.y, )
        self.map_frame.place(relx=0.5, rely=0.5, anchor="center")

    def _on_enter_scene(self):
        self.start_game(SettingManager.grid_size)

    def start_game(self, grid_size: Vector2I):
        assert grid_size.x > 0
        assert grid_size.y > 0
        self.size = grid_size
        self._grid = [
            # * Generate tiles and give position data
            [Tile(Vector2I(x, y)) for x in range(self.size.y)] for y in range(self.size.x)]

        for y in range(self.size.y):
            for x in range(self.size.x):
                btn = Button(text=f"{x}-{y}")
                btn.grid(in_= self.map_frame)

    def cleanup(self):
        self.size = None
        self._grid = None

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]
