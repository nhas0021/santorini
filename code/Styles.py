# https://coolors.co/palette/22223b-4a4e69-9a8c98-c9ada7-f2e9e4
# https://www.tcl-lang.org/man/tcl8.4/TkCmd/colors.htm
import tkinter as tk
from tkinter import Frame
from typing import Callable
from MathLib.Vector import Vector2I

# region Colours
# region Debug
DEBUG_ERR_COLOUR: str = "magenta"
DEBUG_SPRITE_OUTLINE_COLOUR: str = "red1"
DEBUG_SPRITE_AREA_COLOUR: str = "green1"
# endregion

# ~ Game Colors
BG_COLOUR: str = "#22223B"
BG_SUB_COLOUR: str = "#4A4E69"

TEXT_COLOUR: str = "#F2E9E4"

WHITE: str = "#FFFFFF"
BLACK: str = "#000000"


WATER_COLOUR: str = "#0b5394"
SAND_COLOUR: str = "#ffe599"
DIRT_COLOUR: str = "#e0b97b"
GRASS_COLOUR: str = "#6aa84f"
STACK_COLOUR: str = "#fbfbfb"
DOME_COLOUR: str = "#dadada"
PLAYER_COLORS = ["#f44336", "#2986cc", "#f6b26b"]  # * red, blue, orange
POP_UP_COLOR: str = "#FFFACD"
# endregion

# region Game Sizes
# * These are the sizes at 1920x1080 (native), which can then be scaled
TILE_SIZE = Vector2I(100, 100)
WORKER_POSITIONS = (
    40,
    30,
    20
)

WORKER_WIDTH_PX = 10
WORKER_HEIGHT_PX = 40
# endregion

# region Fonts
FONT_TITLE = "Georgia"
FONT_GENERAL = "Helvetica"
FONT_MAIN_MENU_BUTTON = "Comic Sans MS"
# endregion

# region Generators


def generate_main_menu_button_positive(parent_frame: Frame, text: str, on_click_callback: Callable[[], None]):
    return tk.Button(
        parent_frame,
        text=text,
        font=(FONT_MAIN_MENU_BUTTON, 20),
        bg="#90EE90",                                                # light green
        fg="darkgreen",                                              # text color
        # hover background color
        activebackground="#77DD77",
        activeforeground="white",                                    # hover text color
        borderwidth=4,
        # border color (macOS/Linux)
        highlightbackground="darkgreen",
        # border color focus
        highlightcolor="darkgreen",
        highlightthickness=2,
        # makes the border visible
        relief="solid",
        width=10,
        command=on_click_callback
    )


def generate_main_menu_button_negative(parent_frame: Frame, text: str, on_click_callback: Callable[[], None]):
    return tk.Button(
        parent_frame,
        text=text,
        font=(FONT_MAIN_MENU_BUTTON, 20),
        bg="#FF7F7F",                                                # light red
        fg="BLACK",                                                  # text color
        # hover background color
        activebackground="coral1",
        activeforeground="white",                                    # hover text color
        borderwidth=4,
        # makes the border visible
        relief="solid",
        width=10,
        command=on_click_callback
    )
# endregion
