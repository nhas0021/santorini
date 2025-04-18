import tkinter as tk
from Game import MatchData
from MathLib.Vector import Vector2I
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

        self.frame.config(background=WHITE)

        # ! Change this later the placements/styles of these later
        self.text_title = tk.Label(
        self.frame,
        text="Santorini",
        bg=WHITE,
        fg=BLACK,
        font=("Georgia", 45, "bold underline"),
        justify="center"
        )
        self.text_title.place(relx=0.5, rely=0.1, anchor="center")

        self.button_play = tk.Button(
            self.frame, text="Play", font=("Comic Sans MS", 20), 
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth= 4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width= 10,
            command=lambda: SceneManager.change_scene(SceneID.PRE_GAME))
        self.button_play.place(relx=0.2, rely=0.25, anchor="w")

        self.button_tutorial = tk.Button(
            self.frame, text="Tutorial", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth= 4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width= 10,
            command=lambda: SceneManager.change_scene(SceneID.TUTORIAL))
        self.button_tutorial.place(relx=0.2, rely=0.4, anchor="w")

        self.button_rulebook = tk.Button(
            self.frame, text="Rule Book", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth= 4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width= 10,
            command=lambda: SceneManager.change_scene(SceneID.RULEBOOK))
        self.button_rulebook.place(relx=0.2, rely=0.55, anchor="w")

        self.button_settings = tk.Button(
            self.frame, text="Settings", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth= 4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width= 10,
            command=lambda: SceneManager.change_scene(SceneID.SETTINGS))
        self.button_settings.place(relx=0.2, rely=0.7, anchor="w")

        self.button_quit = tk.Button(
            # ! replace with proper shutdown
            self.frame, text="Quit", font=("Comic Sans MS", 20),
            bg="#FF7F7F",        # light green
            fg=BLACK,      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth= 4,
            relief="solid",       # makes the border visible
            width= 10)
        self.button_quit.place(relx=0.2, rely=0.85, anchor="w")

        # image
        self.board_image = tk.PhotoImage(file="code/Assets/santorini.png")  # Replace with your image path
        self.image_label = tk.Label(self.frame, image=self.board_image, bg=WHITE)
        self.image_label.place(relx=0.7, rely=0.6, anchor="center")


class CharacterSelect(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # TODO: Assign match data to a global state
        # match = MatchData(2, Vector2I(5, 5))

