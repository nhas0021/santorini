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


class GameScene(Scene):
    def __init__(self, root: Tk, map_render_size: Vector2I) -> None:
        super().__init__(root)
        self.frame.config(background=WATER_COLOUR)

        self.size: Optional[Vector2I] = None
        # ! Note: Acess should be [x][y].
        self._grid: Optional[list[list[Tile]]] = None
        self.map_frame: Frame = Frame(
            self.frame, width=map_render_size.x, height=map_render_size.y, bg=DIRT_COLOUR, highlightthickness=15, highlightbackground=SAND_COLOUR)
        self.map_frame.place(relx=0.5, rely=0.5, anchor="center")

    def on_enter_scene(self):
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
                tile_size = Vector2I(100, 100)  # TODO TEMP MAYBE
                canvas = Canvas(self.map_frame, width=tile_size.x,
                                height=tile_size.y, bg=GRASS_COLOUR, highlightthickness=0)
                canvas.grid(row=y, column=x, padx=5, pady=5)

                # region TEMP
                # TODO - change to use image or a proper generator later
                stack_grow_bottom_offset = 10
                stack_grow_from_centre = tile_size.x//2
                stack_height = 15

                # * Stacks
                s1 = canvas.create_rectangle(stack_grow_from_centre + 40, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*0, stack_grow_from_centre-40, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*1, fill=STACK_COLOUR)
                s2 = canvas.create_rectangle(stack_grow_from_centre + 30, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*1, stack_grow_from_centre-30, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*2, fill=STACK_COLOUR)
                s3 = canvas.create_rectangle(stack_grow_from_centre + 20, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*2, stack_grow_from_centre-20, tile_size.y - stack_grow_bottom_offset -
                                             stack_height*3, fill=STACK_COLOUR)

                t = canvas.create_text(
                    stack_grow_from_centre, tile_size.y - stack_grow_bottom_offset, anchor="s", text="?", justify="center", fill=TEXT_COLOUR)

                # * Dome
                d = canvas.create_arc(stack_grow_from_centre + 20, tile_size.y - stack_grow_bottom_offset -
                                      stack_height*2, stack_grow_from_centre-20, tile_size.y - stack_grow_bottom_offset -
                                      stack_height*4, start=0, extent=180, fill=DOME_COLOUR)

                # * Worker (colour change for different players)
                w_y = tile_size.y - stack_grow_bottom_offset - stack_height*3  # change this for each stack
                w = canvas.create_oval(stack_grow_from_centre + 10, w_y,
                                       stack_grow_from_centre - 10, w_y - 40, fill=DEBUG_ERR_COLOUR)

                def on_canvas_click(e) -> None:
                    print(e)
                canvas.bind("<Button-1>", on_canvas_click)
                # endregion

        # a = [[Button(self.map_frame, text=f"{x}-{y}")
        #       for x in range(self.size.y)] for y in range(self.size.x)]

    def cleanup(self):
        self.size = None
        self._grid = None

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]
