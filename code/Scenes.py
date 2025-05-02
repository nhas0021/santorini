"""
General Scenes go here, more complicated scenes should be moved to their own file
"""
from random import sample
import tkinter as tk
from typing import cast
from God import God
from SceneID import SceneID
from Preferences import Preferences
from Assets.Styles import *
from Assets.AssetLoader import *

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


class Title (Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.start_bg_button = tk.Button(
            self.frame, bg=BG_COLOUR, activebackground=BG_SUB_COLOUR, borderwidth=0, text="Click anywhere to start...", font=(FONT_GENERAL, 36),  fg=WHITE, justify="center", command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU))
        self.start_bg_button.pack(fill="both", expand=True)

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
            font=(FONT_TITLE, 45, "bold underline"),
            justify="center"
        )
        self.text_title.place(relx=0.5, rely=0.1, anchor="center")

        self.button_play = generate_main_menu_button_positive(
            self.frame, "Play", lambda: SceneManager.change_scene(SceneID.PRE_GAME))
        self.button_play.place(relx=0.2, rely=0.25, anchor="w")

        self.button_tutorial = generate_main_menu_button_positive(
            self.frame, "Tutorial", lambda: SceneManager.change_scene(SceneID.TUTORIAL))
        self.button_tutorial.place(relx=0.2, rely=0.4, anchor="w")

        self.button_rulebook = generate_main_menu_button_positive(
            self.frame, "Rule Book", lambda: SceneManager.change_scene(SceneID.RULEBOOK))
        self.button_rulebook.place(relx=0.2, rely=0.55, anchor="w")

        self.button_settings = generate_main_menu_button_positive(
            self.frame, "Settings", lambda: SceneManager.change_scene(SceneID.SETTINGS))
        self.button_settings.place(relx=0.2, rely=0.7, anchor="w")

        self.button_quit = generate_main_menu_button_negative(
            self.frame, "Quit", root.destroy)
        self.button_quit.place(relx=0.2, rely=0.85, anchor="w")

        # image
        # Replace with your image path
        self.board_image = tk.PhotoImage(data=cast(bytes, logo_bin))
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
            font=(FONT_TITLE, 32, "bold"),
            bg=WHITE,
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        # Info Display (not editable yet)
        self.info_text = tk.Label(
            self.frame,
            text=f"Number of Players: {Preferences.player_count}\nGrid Size: {Preferences.grid_size.x} x {Preferences.grid_size.y}",
            font=(FONT_GENERAL, 16),
            bg=WHITE,
            fg="#333333",
            justify="center"
        )
        self.info_text.pack(pady=20)

        # Instruction
        self.instructions_label = tk.Label(
            self.frame,
            text="Click below to assign gods and start the game.",
            font=(FONT_GENERAL, 14),
            bg=WHITE
        )
        self.instructions_label.pack(pady=10)

        # Start Game Button
        self.start_button = tk.Button(
            self.frame,
            text="Attain God Powers",
            font=(FONT_GENERAL, 16, "bold"),
            bg="#4CAF50",
            fg=WHITE,
            padx=20,
            pady=10,
            command=self.confirm_players_and_go_to_assignment
        )
        self.start_button.pack(pady=30)

        # Back button
        self.back_button = tk.Button(
            self.frame,
            text="Back to Main Menu",
            font=(FONT_GENERAL, 16),
            bg="#FF7F7F",
            fg=WHITE,
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU)
        )
        self.back_button.pack(pady=20)

    def confirm_players_and_go_to_assignment(self):
        if Preferences.player_count > len(Preferences.gods_preferences):
            # * if there are more players than stored preferences slots
            while len(Preferences.gods_preferences) < Preferences.player_count:
                # * ensure that there is a preference slot (not yet filled)
                Preferences.gods_preferences.append(None)
        # * now that there are slots make sure they are assigned
        SceneManager.change_scene(SceneID.GOD_ASSIGNMENT)


class GodAssignment(Scene):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.frame.config(background=WHITE)

        self.title_label = tk.Label(
            self.frame,
            text="God Assignment",
            font=(FONT_TITLE, 28, "bold"),
            bg=WHITE,
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        self.info_label = tk.Label(
            self.frame,
            text="Gods are being assigned randomly to players...",
            font=(FONT_GENERAL, 14),
            bg=WHITE
        )
        self.info_label.pack(pady=10)

        self.assign_button = tk.Button(
            self.frame,
            text="Assign Gods",
            font=(FONT_GENERAL, 16, "bold"),
            bg="#4CAF50",
            fg=WHITE,
            padx=20,
            pady=10,
            command=self.random_assign_god_preferences  # ! random for now
        )
        self.assign_button.pack(pady=30)

        self.result_frame = tk.Frame(self.frame, bg=WHITE)
        self.result_frame.pack(pady=10)

        self.start_game_button = tk.Button(
            self.frame,
            text="Start Game",
            font=(FONT_GENERAL, 16, "bold"),
            bg="#1E88E5",
            fg=WHITE,
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.GAME)
        )
        self.start_game_button.pack(pady=20)
        self.start_game_button.config(state=tk.DISABLED)
        # Back button
        self.back_button = tk.Button(
            self.frame,
            text="Back to Pre-Game",
            font=(FONT_GENERAL, 16),
            bg="#FF7F7F",
            fg=WHITE,
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.PRE_GAME)
        )
        self.back_button.pack(pady=20)

    def random_assign_god_preferences(self):
        assert Preferences.player_count <= len(
            Preferences.gods_selectable), "There are not enough heros to uniquely assign each player a different one"

        randomly_selected_gods = sample(
            # ? can also add weights
            Preferences.gods_selectable, Preferences.player_count)

        for i in range(len(Preferences.gods_preferences)):
            # * apply the random allocation
            Preferences.gods_preferences[i] = randomly_selected_gods[i]

        self.info_label.config(text="Gods assigned! See below:")

        # Clear old results if assignment button is clicked again
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        for i in range(len(Preferences.gods_preferences)):
            assert Preferences.gods_preferences[i]
            # ! Note: this was asserted to exist above
            prefered_god_type = cast(God, Preferences.gods_preferences[i])

            player_label = tk.Label(
                self.result_frame,
                text=f"Player {i+1} ➝ {prefered_god_type.NAME}",
                font=(FONT_GENERAL, 14),
                bg=WHITE,
                fg="#333333"
            )
            player_label.pack(anchor="w", pady=5)

        self.start_game_button.config(state=tk.NORMAL)

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
            font=(FONT_TITLE, 28, "bold"),
            bg=WHITE,
            fg="#2E2E2E"
        )
        self.title_label.pack(pady=30)

        # Rule book content (placeholder text)
        self.rules_text = tk.Text(
            self.frame,
            wrap="word",
            font=(FONT_GENERAL, 14),
            bg=WHITE,
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
            font=(FONT_GENERAL, 16),
            bg="#FF7F7F",
            fg=WHITE,
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU)
        )
        self.back_button.pack(pady=20)
