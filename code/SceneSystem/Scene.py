import tkinter as tk
from tkinter import Frame
from Styles import *


class Scene:
    """
    A frame that covers a whole screen (can be thought of as a phase of the application)
    """

    def __init__(self, root: tk.Tk) -> None:
        self.frame: Frame = Frame(
            root, bg=ERR_COLOUR)

    def disable_scene(self):
        self.frame.pack_forget()

    def enable_scene(self):
        self.frame.pack_configure(fill="both", expand=True)
