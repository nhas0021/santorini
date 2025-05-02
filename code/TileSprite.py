from tkinter import HIDDEN, Canvas, Event, Frame
from typing import Callable
from MathLib.Vector import Vector2I
from Styles import *


class TileSprite:
    """
    Tile UI (logic is in LogicTile)
    Defaults are what a tile is before anything happens on them.

    This tile generates the shapes instead of compositing using images, this for sprint 2 (to be changed in sprint 3)
    """

    def __init__(self, parent_frame: Frame, position: Vector2I, on_click_callback: Callable[["Event[Canvas]"], None]) -> None:
        # ! Gameplay Data
        self.position: Vector2I = position
        # ! Sprite / Data
        self.stack_height_px: int = 15
        self.scaled_tile_size = TILE_SIZE  # TODO add scaling
        # ? Note: some of this might be better suited in styles

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
            self.canvas.create_rectangle(canvas_centre + stack_widths[0], stack_grow_from_y - self.stack_height_px*0,
                                         canvas_centre -
                                         stack_widths[0], stack_grow_from_y -
                                         self.stack_height_px*1,
                                         fill=STACK_COLOUR),
            self.canvas.create_rectangle(canvas_centre + stack_widths[1], stack_grow_from_y - self.stack_height_px*1,
                                         canvas_centre -
                                         stack_widths[1], stack_grow_from_y -
                                         self.stack_height_px*2,
                                         fill=STACK_COLOUR),
            self.canvas.create_rectangle(canvas_centre + stack_widths[2], stack_grow_from_y - self.stack_height_px*2,
                                         canvas_centre -
                                         stack_widths[2], stack_grow_from_y -
                                         self.stack_height_px*3,
                                         fill=STACK_COLOUR)
        ]
        for sprite in self.stack_sprites:
            self.canvas.itemconfig(sprite, state=HIDDEN)

        # * Dome
        dome_width = 20
        self.dome_sprite = self.canvas.create_arc(canvas_centre + dome_width,  # type: ignore[PylancereportUnknownMemberType] #! tkinter badly typed
                                                  stack_grow_from_y - self.stack_height_px*2,
                                                  canvas_centre - dome_width,
                                                  stack_grow_from_y - self.stack_height_px*4,
                                                  start=0, extent=180, fill=DOME_COLOUR)
        self.canvas.itemconfig(self.dome_sprite, state=HIDDEN)

        # * Worker (colour change for different players)
        worker_pos_y = stack_grow_from_y

        # * Note: Change colours for different players rather than make a new one
        self.worker_sprite = self.canvas.create_oval(canvas_centre + WORKER_WIDTH_PX,
                                                     worker_pos_y,
                                                     canvas_centre - WORKER_WIDTH_PX,
                                                     worker_pos_y - WORKER_HEIGHT_PX,
                                                     fill=DEBUG_ERR_COLOUR)
        self.canvas.itemconfig(self.worker_sprite, state=HIDDEN)

        self.canvas.bind(
            # ! Ensure that only the current (as of binding) values are stored
            "<Button-1>", on_click_callback)
        # endregion
