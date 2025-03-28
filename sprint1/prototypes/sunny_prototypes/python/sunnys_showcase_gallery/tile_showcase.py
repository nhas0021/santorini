# proto 2
from tkinter import Label, Tk, Frame, Canvas
from PIL import Image, ImageTk

from global_data import PATH_ASSET

GRID_SIZE = 5
TILE_SIZE = 128
TILE_GRASS = Image.open(
    PATH_ASSET+"/art/kenney_block-pack/PNG/Double (128px)/tileGrass.png").crop((0, 52, 128, 200))


def main():
    # Create an instance of tkinter frame
    win = Tk()
    tile_floor = ImageTk.PhotoImage(TILE_GRASS)

    frame = Frame(win)
    frame.pack()

    canvas = Canvas(frame, bg="black", width=2000, height=2000)
    canvas.pack()

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            canvas.create_image(500 + col*(128), 500 +
                                row*(128-40), image=tile_floor)

    win.mainloop()


if __name__ == '__main__':
    main()
