"""
General Scenes go here, more complicated scenes should be moved to their own file
"""
import tkinter as tk
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
from Styles import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager
from GameManager import GameManager


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
            borderwidth=4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width=10,
            command=lambda: SceneManager.change_scene(SceneID.PRE_GAME))
        self.button_play.place(relx=0.2, rely=0.25, anchor="w")

        self.button_tutorial = tk.Button(
            self.frame, text="Tutorial", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth=4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width=10,
            command=lambda: SceneManager.change_scene(SceneID.TUTORIAL))
        self.button_tutorial.place(relx=0.2, rely=0.4, anchor="w")

        self.button_rulebook = tk.Button(
            self.frame, text="Rule Book", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth=4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width=10,
            command=lambda: SceneManager.change_scene(SceneID.RULEBOOK))
        self.button_rulebook.place(relx=0.2, rely=0.55, anchor="w")

        self.button_settings = tk.Button(
            self.frame, text="Settings", font=("Comic Sans MS", 20),
            bg="#90EE90",        # light green
            fg="darkgreen",      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth=4,
            highlightbackground="darkgreen",  # border color (macOS/Linux)
            highlightcolor="darkgreen",       # border color focus
            highlightthickness=2,
            relief="solid",       # makes the border visible
            width=10,
            command=lambda: SceneManager.change_scene(SceneID.SETTINGS))
        self.button_settings.place(relx=0.2, rely=0.7, anchor="w")

        self.button_quit = tk.Button(
            self.frame, text="Quit", font=("Comic Sans MS", 20),
            bg="#FF7F7F",        # light green
            fg=BLACK,      # text color
            activebackground="#77DD77",  # hover background color
            activeforeground="white",    # hover text color
            borderwidth=4,
            relief="solid",       # makes the border visible
            width=10,
            command=root.destroy)  # Properly shuts down the application
        self.button_quit.place(relx=0.2, rely=0.85, anchor="w")

        # image
        # Replace with your image path
        self.board_image = tk.PhotoImage(file="Assets/santorini.png")
        self.image_label = tk.Label(
            self.frame, image=self.board_image, bg=WHITE)
        self.image_label.place(relx=0.7, rely=0.6, anchor="center")


class PreGame(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.frame.config(background=WHITE)

        # Game setup values (fixed for now, give option to change later)
        # Title
        self.title_label = tk.Label(
            self.frame,
            text="Santorini - Game Setup",
            font=("Georgia", 32, "bold"),
            bg="#ffffff",
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        # Info Display (not editable yet)
        self.info_text = tk.Label(
            self.frame,
            text=f"Number of Players: {SettingManager.player_count}\nGrid Size: {SettingManager.grid_size.x} x {SettingManager.grid_size.y}",
            font=("Helvetica", 16),
            bg="#ffffff",
            fg="#333333",
            justify="center"
        )
        self.info_text.pack(pady=20)

        # Instruction
        self.instructions_label = tk.Label(
            self.frame,
            text="Click below to assign gods and start the game.",
            font=("Helvetica", 14),
            bg="#ffffff"
        )
        self.instructions_label.pack(pady=10)

        # Start Game Button
        self.start_button = tk.Button(
            self.frame,
            text="Attain God Powers",
            font=("Helvetica", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.start_god_assignment
        )
        self.start_button.pack(pady=30)

        # Back button
        self.back_button = tk.Button(
            self.frame,
            text="Back to Main Menu",
            font=("Helvetica", 16),
            bg="#FF7F7F",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU)
        )
        self.back_button.pack(pady=20)

    def start_god_assignment(self):
        GameManager.setup_game()

        # Go to the god assignment scene
        SceneManager.change_scene(SceneID.GOD_ASSIGNMENT)


class GodAssignment(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.frame.config(background=WHITE)

        self.title_label = tk.Label(
            self.frame,
            text="God Assignment",
            font=("Georgia", 28, "bold"),
            bg="#ffffff",
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        self.info_label = tk.Label(
            self.frame,
            text="Gods are being assigned randomly to players...",
            font=("Helvetica", 14),
            bg="#ffffff"
        )
        self.info_label.pack(pady=10)

        self.assign_button = tk.Button(
            self.frame,
            text="Assign Gods",
            font=("Helvetica", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self.assign_gods
        )
        self.assign_button.pack(pady=30)

        self.result_frame = tk.Frame(self.frame, bg="#ffffff")
        self.result_frame.pack(pady=10)

        self.start_game_button = tk.Button(
            self.frame,
            text="Start Game",
            font=("Helvetica", 16, "bold"),
            bg="#1E88E5",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.GAME)
        )
        self.start_game_button.pack(pady=20)
        # TODO: Hide until gods are assigned
        self.start_game_button.config(state=tk.NORMAL)
        # Back button
        self.back_button = tk.Button(
            self.frame,
            text="Back to Pre-Game",
            font=("Helvetica", 16),
            bg="#FF7F7F",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.PRE_GAME)
        )
        self.back_button.pack(pady=20)

    def assign_gods(self):
        GameManager.get_game().assign_gods_random_from_list()

        self.info_label.config(text="Gods assigned! See below:")

        # Clear old results if assignment button is clicked again
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for player in GameManager.get_game().players:
            player_label = tk.Label(
                self.result_frame,
                text=f"Player {player.id} ➝ {player.god.name}",
                font=("Helvetica", 14),
                bg="#ffffff",
                fg="#333333"
            )
            player_label.pack(anchor="w", pady=5)

        self.start_game_button.config(state="normal")

    def start_game(self):
        # not a registered secne yet so throws an error
        SceneManager.change_scene(SceneID.GAME)


class RuleBook(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.frame.config(background=WHITE)

        self.title_label = tk.Label(
            self.frame,
            text="Rule Book",
            font=("Georgia", 28, "bold"),
            bg="#ffffff",
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        # Rule book content (placeholder text)
        self.rules_text = tk.Text(
            self.frame,
            wrap="word",
            font=("Helvetica", 14),
            bg="#ffffff",
            fg="#333333",
            height=20,
            width=80
        )
        self.rules_text.pack(pady=10)

        # Sample rules (replace with actual rules)
        sample_rules = (
            "1. Each player takes turns placing a worker on the board.\n"
            "2. Players can build on the board to create structures.\n"
            "3. The goal is to reach the third level of a structure.\n"
            "4. Players can use god powers to gain advantages.\n"
        )

        self.rules_text.insert(tk.END, sample_rules)
        self.rules_text.config(state="disabled")  # Make it read-only

        # Back button
        self.back_button = tk.Button(
            self.frame,
            text="Back to Main Menu",
            font=("Helvetica", 16),
            bg="#FF7F7F",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU)
        )
        self.back_button.pack(pady=20)
