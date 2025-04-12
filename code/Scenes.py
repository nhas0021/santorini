import tkinter as tk
from SceneID import SceneID
from Styles import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


class Title (Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.start_bg_button = tk.Button(
            self.frame, bg=BG_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU))
        self.start_bg_button.pack(fill="both", expand=True)

        self._start_text = tk.Label(
            self.frame, bg=BG_COLOUR, text="Click anywhere to start...", fg=TEXT_COLOUR, justify="center")
        self._start_text.place(relx=0.5, rely=0.5, anchor="center")


class MainMenu(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
