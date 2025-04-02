
# Proto 3

from tkinter import Label, Tk, Frame, Canvas
from PIL import Image, ImageTk
from pathlib import Path

from global_data import PATH_ASSET

# region~ Classes


class Tile:
    def __init__(self, height: int = 0):
        self.height = height
# endregion


# region~ Consts
GRID_SIZE = 5
TILE_SIZE = 128
# endregion


# region~ Program
def main():
    # ~ Init data
    TEMP_map_seed = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [0, 3, 0, 1, 0],
        [0, 0, 0, 0, 0]]
    map_state: list[list[Tile]] = []

    temp = []
    for row in range(GRID_SIZE):
        r = []
        for col in range(GRID_SIZE):
            r.append(Tile(TEMP_map_seed[col][row]))
        map_state.append(r)

    # region~ Init Window
    win = Tk()
    frame = Frame(win)
    frame.pack()

    canvas = Canvas(frame, bg="black", width=2000, height=2000)
    canvas.pack()
    # endregion

    # region~ Resources
    TILE_FLOOR = ImageTk.PhotoImage(Image.open(
        Path(PATH_ASSET + "/art/kenney_block-pack/PNG/Double (128px)/tileGrass.png")).crop((0, 52, 128, 200)))

    TILE_LEVEL = (
        ImageTk.PhotoImage(Image.open(
            Path(PATH_ASSET + "/art/kenney_block-pack/PNG/Double (128px)/tileCastle_gate.png")).crop((0, 52, 128, 200))),
        ImageTk.PhotoImage(Image.open(
            Path(PATH_ASSET + "/art/kenney_block-pack/PNG/Double (128px)/tileCastle.png")).crop((0, 52, 128, 200))),
        ImageTk.PhotoImage(Image.open(Path(PATH_ASSET + "./art/kenney_block-pack/PNG/Double (128px)/tileCastle_top.png")).crop((0, 52, 128, 200))))

    TILE_LEVEL_OFFSETS = (-60, -120, -180, -180)

    # last level just replaces top with a top+spike
    TILE_LEVEL_FINAL = Image.open(
        Path(PATH_ASSET + "/art/kenney_block-pack/PNG/Double (128px)/tileCastle_topRoof.png")).crop((0, 52, 128, 200))
    # endregion

    # * render
    # dont need z-buffer but aware draw order
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # can have 40 or 44 depends
            local_pos = (500 + col*(128), 500 + row*(128-40))
            canvas.create_image(local_pos, image=TILE_FLOOR)  # floor

            for i in range(map_state[col][row].height):
                canvas.create_image(
                    local_pos[0], local_pos[1] + TILE_LEVEL_OFFSETS[i], image=TILE_LEVEL[i])

    win.mainloop()
# endregion


if __name__ == '__main__':
    main()
