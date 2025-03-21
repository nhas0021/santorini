# proto 1
from tkinter import Tk, Frame, Canvas
from PIL import Image, ImageTk
from pathlib import Path

from global_data import PATH_ASSET


def main():
    t = Tk()
    t.title("Transparency")

    frame = Frame(t)
    frame.pack()

    canvas = Canvas(frame, bg="black", width=500, height=500)
    canvas.pack()

    photoimage = ImageTk.PhotoImage(
        file=Path(PATH_ASSET + "/art/kenney_block-pack/PNG/Double (128px)/tileGrass.png"))
    canvas.create_image(150, 150, image=photoimage)

    t.mainloop()


if __name__ == '__main__':
    main()
