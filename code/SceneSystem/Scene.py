import tkinter as tk
from tkinter import Frame
from Assets.Styles import DEBUG_ERR_COLOUR


class Scene:
    """
    A scene/level can be thought of as a phase of the application)
    """

    def __init__(self, root: tk.Tk) -> None:
        self.frame: Frame = Frame(
            root, bg=DEBUG_ERR_COLOUR)

    def disable_scene(self):
        """Remove the scene from being rendered/interacted with, does not remove from memory."""
        self.frame.pack_forget()

    def enable_scene(self):
        """Show the scene and allow it to be interacted with."""
        self.frame.pack_configure(fill="both", expand=True)

    def on_enter_scene(self): """Override this. Triggers when entering the scene."""
    def on_exit_scene(self): """Override this. Triggers when exiting the scene."""


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
