import tkinter as tk
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
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

        # ! Change this later the placements/styles of these later
        self.text_title = tk.Label(
            self.frame, bg=BG_COLOUR, text="Santorini", fg=TEXT_COLOUR, justify="center")
        self.text_title.place(anchor="center")

        self.button_play = tk.Button(
            self.frame, text="Play", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.PRE_GAME))
        self.button_play.pack()

        self.button_tutorial = tk.Button(
            self.frame, text="Tutorial", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.TUTORIAL))
        self.button_tutorial.pack()

        self.button_rulebook = tk.Button(
            self.frame, text="Rule Book", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.RULEBOOK))
        self.button_rulebook.pack()

        self.button_settings = tk.Button(
            self.frame, text="Settings", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.SETTINGS))
        self.button_settings.pack()

        self.button_quit = tk.Button(
            # ! replace with proper shutdown
            self.frame, text="Quit", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: exit(0))
        self.button_quit.pack()


class CharacterSelect(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # TODO: get this from user input
        __map_size = Vector2I(5, 5)
        __map_render_size = Vector2I(500, 500)

        # ! Set with chosen data
        SettingManager.grid_size = __map_size
        SettingManager.map_frame_size = __map_render_size

        self.button_play = tk.Button(
            self.frame, text="WIP - PLAY WITH DEFAULTS", bg=BG_SUB_COLOUR, borderwidth=0, command=lambda: SceneManager.change_scene(SceneID.GAME))
        self.button_play.pack()
