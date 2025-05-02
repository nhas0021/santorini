import tkinter as tk
from tkinter import Frame
from Assets.Styles import *


class Scene:
    """
    A frame that covers a whole screen (can be thought of as a phase of the application)
    """

    def __init__(self, root: tk.Tk) -> None:
        self.frame: Frame = Frame(
            root, bg=DEBUG_ERR_COLOUR)

    def disable_scene(self):
        self.frame.pack_forget()

    def enable_scene(self):
        self.frame.pack_configure(fill="both", expand=True)

    def on_enter_scene(self): """Override this."""
    def on_exit_scene(self): """Override this."""


# ~ TEMPLATE SCENE
"""
import tkinter as tk
from SceneID import SceneID
from Styles import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager

class SceneName(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
"""
