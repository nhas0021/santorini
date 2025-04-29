# https://coolors.co/palette/22223b-4a4e69-9a8c98-c9ada7-f2e9e4
# https://www.tcl-lang.org/man/tcl8.4/TkCmd/colors.htm
from MathLib.Vector import Vector2I


DEBUG_ERR_COLOUR: str = "magenta"
DEBUG_SPRITE_OUTLINE_COLOUR: str = "red1"
DEBUG_SPRITE_AREA_COLOUR: str = "green1"

BG_COLOUR: str = "#22223B"
BG_SUB_COLOUR: str = "#4A4E69"

TEXT_COLOUR: str = "#F2E9E4"

WHITE: str = "#FFFFFF"
BLACK: str = "#000000"


# ~ Game Colors
WATER_COLOUR: str = "#0b5394"
SAND_COLOUR: str = "#ffe599"
DIRT_COLOUR: str = "#e0b97b"
GRASS_COLOUR: str = "#6aa84f"
STACK_COLOUR: str = "#fbfbfb"
DOME_COLOUR: str = "#dadada"
PLAYER_COLORS = ["#f44336", "#2986cc", "#f6b26b"]  # red, blue, orange

# ~ Game Sizes
# * These are the sizes at 1920x1080 (native), which can then be scaled
TILE_SIZE = Vector2I(100, 100)
WORKER_POSITIONS = (
    40,
    30,
    20
)

WORKER_WIDTH_PX = 10
WORKER_HEIGHT_PX = 40
