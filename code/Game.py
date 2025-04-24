from dataclasses import dataclass
from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame
from typing import Callable, List, Optional, Tuple
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
from Styles import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


class Tile:
    """
    Defaults are what a tile is before anything happens on them.

    This tile generates the shapes instead of compositing using images, this for sprint 2 (to be changed in sprint 3)
    """

    def __init__(self, parent_frame: Frame, position: Vector2I, on_click_callback: Callable[[Event], None]) -> None:
        # ! Gameplay Data
        self.position: Vector2I = position
        self.stack_height: int = 15
        self.worker: int = 0
        # ! Sprite / Data
        # ? Note: some of this might be better suited in styles
        self.stack_sprites: List[int] = []
        self.dome_sprite: int = None
        # * Note: Change colours for different players rather than make a new one
        self.worker_sprite: int = None

        self.scaled_tile_size = TILE_SIZE  # TODO add scaling

        self.canvas = Canvas(parent_frame, width=self.scaled_tile_size.x,
                             height=self.scaled_tile_size.y, bg=GRASS_COLOUR, highlightthickness=0)

        padding = 5
        self.canvas.grid(row=position.y, column=position.x,
                         padx=padding, pady=padding)

        # region TEMP
        # TODO - change to use image
        self.stack_grow_bottom_offset = 10
        stack_grow_from_y = self.scaled_tile_size.y - self.stack_grow_bottom_offset
        canvas_centre = self.scaled_tile_size.x//2

        # * Stacks
        stack_widths = (40, 30, 20)
        self.stack_sprites = [
            self.canvas.create_rectangle(canvas_centre + stack_widths[0], stack_grow_from_y - self.stack_height*0,
                                         canvas_centre -
                                         stack_widths[0], stack_grow_from_y -
                                         self.stack_height*1,
                                         fill=STACK_COLOUR),
            self.canvas.create_rectangle(canvas_centre + stack_widths[1], stack_grow_from_y - self.stack_height*1,
                                         canvas_centre -
                                         stack_widths[1], stack_grow_from_y -
                                         self.stack_height*2,
                                         fill=STACK_COLOUR),
            self.canvas.create_rectangle(canvas_centre + stack_widths[2], stack_grow_from_y - self.stack_height*2,
                                         canvas_centre -
                                         stack_widths[2], stack_grow_from_y -
                                         self.stack_height*3,
                                         fill=STACK_COLOUR)
        ]
        for sprite in self.stack_sprites:
            self.canvas.itemconfig(sprite, state=HIDDEN)

        stack_counter_text = self.canvas.create_text(
            canvas_centre, self.scaled_tile_size.y - self.stack_grow_bottom_offset, anchor="s", text="?", justify="center", fill=TEXT_COLOUR)
        self.canvas.itemconfig(stack_counter_text, state=HIDDEN)

        # * Dome
        dome_width = 20
        self.dome_sprite = self.canvas.create_arc(canvas_centre + dome_width,
                                                  stack_grow_from_y - self.stack_height*2,
                                                  canvas_centre - dome_width,
                                                  stack_grow_from_y - self.stack_height*4,
                                                  start=0, extent=180, fill=DOME_COLOUR)
        self.canvas.itemconfig(self.dome_sprite, state=HIDDEN)

        # * Worker (colour change for different players)
        worker_pos_y = stack_grow_from_y - \
            self.stack_height*3  # change this for each stack
        worker_width = 10
        worker_height = 40
        self.worker_sprite = self.canvas.create_oval(canvas_centre + worker_width,
                                                     worker_pos_y,
                                                     canvas_centre - worker_width,
                                                     worker_pos_y - worker_height,
                                                     fill=DEBUG_ERR_COLOUR)
        self.canvas.itemconfig(self.worker_sprite, state=HIDDEN)

        self.canvas.bind(
            # ! Ensure that only the current (as of binding) values are stored
            "<Button-1>", on_click_callback)
        # endregion


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

    # * Note that tkinter is not fully typed
    def __on_clicked_tile(self, position: Vector2I, e: Event) -> None:
        # TODO replace with game logic
        print(f"{position.x}-{position.y} | {e}")

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]

    def change_stack_visuals(self, tile_position: Vector2I, stack_count: int):
        assert stack_count <= SettingManager.stacks_before_dome+1
        tile = self.get_tile(tile_position)

        for i in range(SettingManager.stacks_before_dome):
            if i <= stack_count-1:  # ? Active stacks
                tile.canvas.itemconfigure(
                    tile.stack_sprites[i], state=NORMAL)  # * show
            else:
                tile.canvas.itemconfigure(
                    tile.stack_sprites[i], state=HIDDEN)  # * hide

        # *Adjust worker pos (don't change visible state)
        tile.canvas.coords(
            tile.worker_sprite,
            tile.scaled_tile_size.x//2,
            tile.scaled_tile_size.y - tile.stack_grow_bottom_offset - tile.stack_height*stack_count)

    def start_game(self, grid_size: Vector2I):
        assert grid_size.x > 0
        assert grid_size.y > 0
        self.size = grid_size
        self._grid = [
            # * Generate tiles and give position data
            [Tile(self.map_frame,  Vector2I(x, y), lambda e, pos=Vector2I(x, y): self.__on_clicked_tile(pos, e)) for x in range(self.size.y)] for y in range(self.size.x)]

    def cleanup(self):
        # TODO reset everything
        # TODO reset UI
        self.size = None
        self._grid = None
