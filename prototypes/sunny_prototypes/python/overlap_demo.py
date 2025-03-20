# proto 1
from tkinter import Tk, Frame, Canvas
from PIL import Image, ImageTk

t = Tk()
t.title("Transparency")

frame = Frame(t)
frame.pack()

canvas = Canvas(frame, bg="black", width=500, height=500)
canvas.pack()

photoimage = ImageTk.PhotoImage(file="./art/kenney_block-pack/PNG/Double (128px)/tileGrass.png")
canvas.create_image(150, 150, image=photoimage)

t.mainloop()