from random import sample
from tkinter import BOTH, NORMAL, HIDDEN, Tk, Frame, Label, Toplevel, Button
from typing import Callable, List, Optional
from MapState import MapState
from MathLib.Vector import Vector2I
from Preferences import Preferences
from SceneID import SceneID
from SceneSystem.SceneManager import SceneManager
from Assets.Styles import BLACK, DIRT_COLOUR, FONT_GENERAL, FONT_TITLE, PLAYER_COLORS, POP_UP_COLOR, POPUP_DURATION, SAND_COLOUR, WATER_COLOUR, WHITE, WORKER_HEIGHT_PX, WORKER_WIDTH_PX
from TileSprite import TileSprite
from SceneSystem.Scene import Scene
from TurnManager import Phase, TurnManager
from Worker import Worker


class GameScene(Scene):
    """
    The main scene of the game, holding the renderables, the map data and the turn data.
    """

    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        # ~ initialise data upon entering a scene not during scene creation
        self.turn_manager: TurnManager
        self.map_state: MapState

        # ~ initialise visuals before entering a scene (and hide them)
        # region Initiate Visuals
        # region Generate background / environment sprites
        self.frame.config(background=WATER_COLOUR)

        # ! Note: Access should be [x][y].
        self._sprite_tilemap: Optional[list[list[TileSprite]]] = None

        self.map_frame: Frame = Frame(
            self.frame,
            width=Preferences.map_frame_size_px.x,
            height=Preferences.map_frame_size_px.y,
            bg=DIRT_COLOUR, highlightthickness=15,
            highlightbackground=SAND_COLOUR)

        self.map_frame.place(relx=0.5, rely=0.5, anchor="center")
        # endregion
        # region Generate popups
        # ? A skip
        self.skip_action_button = Button(
            self.frame,
            text="Skip",
            font=("Arial", 18, "bold"),  # Make the text bold and larger
            bg="red",  # Set the background color to something prominent
            fg="white",  # Set the text color to white
            padx=20,  # Add padding to the sides of the button
            pady=10,  # Add padding to the top and bottom of the button
            bd=5,  # Add a border to make it stand out more
            relief="raised",  # Raised effect for a 3D button
        )

        # ? Shows the current game phase
        self.info_panel = Frame(
            self.frame, width=200, height=200, bg=POP_UP_COLOR, bd=2, relief="solid")
        self.info_panel.place(relx=0.05, rely=0.3, anchor="w")

        # ? Label inside the info panel
        self.phase_info_label = Label(
            self.info_panel,
            text="",
            font=(FONT_GENERAL, 12, "bold"),
            bg=POP_UP_COLOR,
            fg="#333",
            wraplength=180,
            justify="center"
        )
        self.phase_info_label.place(relx=0.5, rely=0.5, anchor="center")

        # ? Label for God info
        self.god_panel = Frame(
            self.frame, width=200, height=200, bg=POP_UP_COLOR, bd=2, relief="solid")
        self.god_panel.place(relx=0.05, rely=0.7, anchor="w")

        self.god_info_label = Label(
            self.god_panel,
            text="",
            font=(FONT_GENERAL, 12, "bold"),
            bg=POP_UP_COLOR,
            fg="#333",
            wraplength=180,
            justify="center"
        )
        self.god_info_label.place(relx=0.5, rely=0.5, anchor="center")
        # endregion
        # region Generate Match Result Overlay
        # ? The frame which the "game over" overlay consists of
        self.match_result_overlay = Frame(self.frame, bg=WHITE)

        self.match_result_overlay.pack(fill=BOTH, expand=True)

        self.match_result_overlay.pack_forget()  # * hide it

        self.title_label = Label(
            self.match_result_overlay,
            text="Game Over",
            font=(FONT_TITLE, 36, "bold"),
            bg=WHITE,
            fg="#FF0000"
        )

        # ? Game Over Title
        self.title_label.pack(pady=40)

        # Winner label (created once here)
        self.winner_label = Label(
            self.match_result_overlay,
            text="",  # Will be set later
            font=(FONT_GENERAL, 24, "bold"),
            bg=WHITE,
            fg="#2E8B57"
        )
        self.winner_label.pack(pady=20)

        # ? Return to Main Menu button
        self.main_menu_button = Button(
            self.match_result_overlay,
            text="Return to Main Menu",
            font=(FONT_GENERAL, 16),
            bg="#ADD8E6",
            fg=BLACK,
            padx=20,
            pady=10,
            command=lambda: SceneManager.change_scene(SceneID.MAIN_MENU)
        )
        self.main_menu_button.pack(pady=30)

        # endregion
        # endregion
        return

    def enable_skip_button(self, action: Callable[[], None]):
        """Attach and action to this button which is used to skip an optional action."""
        print("[Notice] Can skip this action.")
        self.skip_action_button.config(command=action)
        self.skip_action_button.place(relx=1, rely=1, anchor="se")

    def disable_skip_button(self):
        """Disable this button"""
        self.skip_action_button.config(command=lambda: None)
        self.skip_action_button.place_forget()

    def show_match_result(self):
        """Show the match results, will display who won"""
        assert self.turn_manager
        assert self.turn_manager.winner
        self.match_result_overlay.pack(fill=BOTH, expand=True)

        self.winner_label.config(
            text=f"🎉 Player {self.turn_manager.winner.id + 1} Wins! 🎉"
        )

    def match_over(self):
        """Event that is triggered when match is over"""
        print("[Notice] Match over.")
        # * can add additional actions when needed
        self.show_match_result()

    def place_random_workers(self):
        """
        Randomly place workers in the map, with no overlap
        """
        workers: List[Worker] = []
        for player in self.turn_manager.players:
            workers.extend(player.workers)

        all_possible_positions = [Vector2I(x, y) for x in range(
            self.map_state.size.x) for y in range(self.map_state.size.y)]
        randomised_positions = sample(all_possible_positions, len(workers))

        for worker, position in zip(workers, randomised_positions):
            # link the logic tile to the worker
            self.map_state.get_tile(position).worker = worker
            worker.position = position  # update worker's position
            self.update_tile_visuals(worker.position)

    def on_enter_scene(self):
        # ~ Start-up Game
        # ! load preferences and generate a game state
        # * initialise turn manager and load from preferences
        self.turn_manager = TurnManager(
            Preferences.player_count, Preferences.gods_preferences)
        # * generate map state from preferences
        self.map_state = MapState(
            Preferences.grid_size, Preferences.max_stacks_before_dome)
        self.generate_tilemap_sprites(self.map_state)

        # ! set up for first turn
        self.place_random_workers()
        self.turn_manager.get_current_player().god.on_start_turn(self)
        self.turn_manager.get_current_player().god.on_start_current_phase(self)
        return  # * control released to event calls

    def on_exit_scene(self):
        self.cleanup()
        self.match_result_overlay.pack_forget()

    def generate_tilemap_sprites(self, map_state: MapState):
        """ Generate tilemap sprites based on the map state"""
        assert map_state.size.x > 0
        assert map_state.size.y > 0
        self.map_size = map_state.size
        self._sprite_tilemap = [[
            TileSprite(self.map_frame, Vector2I(x, y),
                       lambda e, pos=Vector2I(x, y): map_state.get_tile(
                           # ? allow the sprite to trigger its linked (and stored) events
                           pos).emit_on_click(e)
                       )
            for y in range(self.map_size.y)] for x in range(self.map_size.x)
        ]

    def get_tile(self, position: Vector2I) -> TileSprite:
        """Accessor for getting a tile using a vector"""
        assert self._sprite_tilemap
        return self._sprite_tilemap[position.x][position.y]

    def update_tile_visuals(self, tile_position: Vector2I, stack_count: Optional[int] = None):
        """
        Updates/refreshes the visuals on the provided tiles, with an option provided to change the stack count of said tile in the process
        """
        # ? Get tile sprite parent and tile data (safely)
        tile_sprite = self.get_tile(tile_position)
        tile_state = self.map_state.get_tile(tile_position)
        # * If stack count provided
        if not stack_count:
            stack_count = tile_state.stack_height
        assert stack_count <= Preferences.max_stacks_before_dome+1

        for i in range(Preferences.max_stacks_before_dome):
            if i <= stack_count-1:
                tile_sprite.canvas.itemconfigure(
                    tile_sprite.stack_sprites[i], state=NORMAL)
            else:
                tile_sprite.canvas.itemconfigure(
                    tile_sprite.stack_sprites[i], state=HIDDEN)

        tile_sprite.canvas.itemconfigure(tile_sprite.dome_sprite, state=(
            NORMAL if stack_count == Preferences.max_stacks_before_dome + 1 else HIDDEN))

        # ! Note: this will still place a worker above a dome even if that is not allowed (this should not need to check)
        worker_centre_x = tile_sprite.scaled_tile_size.x // 2
        worker_centre_y = tile_sprite.scaled_tile_size.y - \
            tile_sprite.stack_grow_bottom_offset - tile_sprite.stack_height_px * stack_count

        tile_sprite.canvas.coords(
            tile_sprite.worker_sprite,
            worker_centre_x + WORKER_WIDTH_PX,
            worker_centre_y,
            worker_centre_x - WORKER_WIDTH_PX,
            worker_centre_y - WORKER_HEIGHT_PX)  # ! may need to scale with ui scaling

        if tile_state.worker:
            tile_sprite.canvas.itemconfig(
                tile_sprite.worker_sprite, fill=PLAYER_COLORS[tile_state.worker.player_id], state=NORMAL)
        else:
            tile_sprite.canvas.itemconfig(
                tile_sprite.worker_sprite, state=HIDDEN)

    def cleanup(self):
        """Is called at the end, clean up the scene so that it can be used again (as if new)"""
        self.map_size = None
        self._sprite_tilemap = None
        self.selected_worker = None
        self.current_phase = Phase.SELECT_WORKER

    def show_player_turn_popup(self):
        """Display a timed popup message which informs which player's turn it is."""
        current_player = self.turn_manager.get_current_player()
        popup = Label(
            self.frame,
            text=f"Player {current_player.id+1}'s Turn!",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def show_cannot_select_worker_popup(self):
        """A warning to show that the action is invalid"""
        popup = Label(
            self.frame,
            text=f"Cannot select another player's worker!",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def show_worker_cannot_move_popup(self):
        """A warning to show that the action is invalid"""
        popup = Label(
            self.frame,
            text=f"This worker cannot move! Please select another worker",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def highlight_current_players_workers(self):
        """Show which workers can be targeted of a specific player"""
        assert self._sprite_tilemap

        # First remove any old highlights
        for row in self._sprite_tilemap:
            for tile in row:
                tile.canvas.itemconfig(tile.worker_sprite, outline="", width=1)

        # Highlight current player's workers
        current_player = self.turn_manager.get_current_player()

        for worker in current_player.workers:
            tile = self.get_tile(worker.position)

            tile.canvas.itemconfig(
                tile.worker_sprite,
                outline="gold",
                width=5
            )

    def highlight_selected_worker(self, worker: Worker):
        """Show which workers can be targeted"""
        assert self._sprite_tilemap
        # * Remove old highlights first
        for row in self._sprite_tilemap:
            for tile in row:
                tile.canvas.itemconfig(tile.worker_sprite, outline="", width=1)

        if not worker:
            return

        # * Highlight the selected worker
        tile = self.get_tile(worker.position)
        tile.canvas.itemconfig(
            tile.worker_sprite,
            outline="red",  # Use blue or any visible color
            width=5
        )

    def show_worker_selected_popup(self):
        """Inform the player what action to take"""
        popup = Label(
            self.frame,
            text=f"Worker Selected! Move your worker...",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # ? Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def show_build_popup(self):
        """Inform the player what action to take"""
        popup = Label(
            self.frame,
            text=f"Worker Moved! Click on an adjacent tile to build...",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def show_invalid_movement_popup(self):
        """Inform the player that the action is invalid"""
        popup = Label(
            self.frame,
            text=f"Worker cannot be moved here! Please try Again.",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def show_invalid_build_popup(self):
        """Inform the player that the action is invalid"""
        popup = Label(
            self.frame,
            text=f"Cannot build here! Please try Again.",
            font=(FONT_GENERAL, 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after delay
        self.frame.after(POPUP_DURATION, popup.destroy)

    def update_phase_info(self):
        """Update the widget with the new turn info"""
        current_player = self.turn_manager.get_current_player()
        text = f"Player {current_player.id + 1}'s Turn\n\n"

        match self.turn_manager.current_phase:
            case Phase.SELECT_WORKER:
                text += "Select one of your workers"
            case Phase.MOVE_WORKER:
                text += "Move the selected worker"
            case Phase.BUILD_STACK:
                text += "Build on an adjacent tile"
            case _:
                text += "Waiting..."

        self.phase_info_label.config(text=text)

    def show_loss_popup(self, player_id: int, reason: str, on_confirm: Callable[[], None]):
        """Show a popup upon reaching a loss condition"""
        popup = Toplevel(self.frame)
        popup.title("Player Eliminated")
        popup.geometry("450x250")
        popup.configure(bg=WHITE)
        popup.grab_set()  # Prevent interaction with main window

        # Header
        title = Label(
            popup,
            text=f"Player {player_id + 1} has been eliminated!",
            font=(FONT_GENERAL, 18, "bold"),
            fg="#FF0000",
            bg=WHITE
        )
        title.pack(pady=(20, 10))

        # Reason
        message = Label(
            popup,
            text=f"Reason: {reason}",
            font=(FONT_GENERAL, 14),
            bg=WHITE,
            wraplength=400,
            justify="center"
        )
        message.pack(pady=10)

        # Continue Button
        continue_btn = Button(
            popup,
            text="Continue",
            font=(FONT_GENERAL, 12),
            command=lambda: self._handle_popup_close(popup, on_confirm)
        )
        continue_btn.pack(pady=20)

    def _handle_popup_close(self, popup: Toplevel, on_confirm: Callable[[], None]):
        """Event that is triggered on to close a popup"""
        popup.destroy()
        on_confirm()  # could be used to continue game with remaining players or show winner

    def show_god_info(self):
        """Enable a card to show god info"""
        current_player = self.turn_manager.get_current_player()
        text = f"God: {current_player.god.NAME}\n\n{current_player.god.DESCRIPTION}"

        self.god_info_label.config(text=text)
