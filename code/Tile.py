from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame
from typing import Callable, List, Optional, Tuple
from MathLib.Vector import Vector2I
from Worker import Worker
from Styles import *

class Tile:
    """
    Defaults are what a tile is before anything happens on them.

    This tile generates the shapes instead of compositing using images, this for sprint 2 (to be changed in sprint 3)
    """

    def __init__(self, parent_frame: Frame, position: Vector2I, on_click_callback: Callable[[Event], None]) -> None:
        # ! Gameplay Data
        self.position: Vector2I = position
        self.stack_height: int = 15
        self.worker: Worker = None
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