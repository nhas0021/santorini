import random
from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame, Label, Toplevel, Button
from typing import Callable, List, Optional, Tuple
from MathLib.Vector import Vector2I
from SettingManager import SettingManager
from Styles import *
from God import God
from Tile import Tile
from enum import Enum, auto

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager
from GameManager import GameManager
from Worker import Worker
from SceneID import SceneID


class Phase(Enum):
    SELECT_WORKER = auto()
    MOVE_WORKER = auto()
    BUILD_STACK = auto()


# TODO: make the Game class hold the grid and not GameScene. use the GameManager to access the grid from the Game here in order to draw it out (this class should only handle UI)
# TODO: Remove any game logic
class GameScene(Scene):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        self.frame.config(background=WATER_COLOUR)

        self.size: Optional[Vector2I] = None

        # ! Note: Acess should be [x][y].
        self._grid: Optional[list[list[Tile]]] = None

        self.map_frame: Frame = Frame(
            self.frame,
            width=SettingManager.map_frame_size.x,
            height=SettingManager.map_frame_size.y,
            bg=DIRT_COLOUR, highlightthickness=15,
            highlightbackground=SAND_COLOUR)

        self.map_frame.place(relx=0.5, rely=0.5, anchor="center")

        # can be select_worker, move_worker, build_stack
        self.current_phase: Phase = Phase.SELECT_WORKER

        #show the current game phase
        self.info_panel = Frame(self.frame, width=200, height=200, bg=POP_UP_COLOR, bd=2, relief="solid")
        self.info_panel.place(relx=0.05, rely=0.3, anchor="w")

        # Label inside the info panel
        self.phase_info_label = Label(
            self.info_panel,
            text="",
            font=("Helvetica", 12, "bold"),
            bg=POP_UP_COLOR,
            fg="#333",
            wraplength=180,
            justify="center"
        )
        self.phase_info_label.place(relx=0.5, rely=0.5, anchor="center")

        # Label for God info
        self.god_panel = Frame(self.frame, width=200, height=200, bg=POP_UP_COLOR, bd=2, relief="solid")
        self.god_panel.place(relx=0.05, rely=0.7, anchor="w")

        self.god_info_label = Label(
            self.god_panel,
            text="",
            font=("Helvetica", 12, "bold"),
            bg=POP_UP_COLOR,
            fg="#333",
            wraplength=180,
            justify="center"
        )
        self.god_info_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_enter_scene(self):
        self.start_game(SettingManager.grid_size)
        self.show_player_turn_popup()
        self.highlight_current_players_workers()
        self.update_phase_info()
        self.show_god_info()

    def on_exit_scene(self):
        self.cleanup()

    # * Note that tkinter is not fully typed
    def __on_clicked_tile(self, position: Vector2I, e: Event) -> None:
        print(
            f"[DEBUG] Clicked on tile at {position.x}-{position.y}, Phase: {self.current_phase}")

        assert GameManager.current_game

        # region Action
        logic_tile = GameManager.current_game.get_tile(position)

        match self.current_phase:
            case Phase.SELECT_WORKER:
                current_player = GameManager.get_game().get_current_player()
                
                if logic_tile.worker:
                    #Check if the worker the player is trying to select is the current player's worker
                    if logic_tile.worker.player_id == current_player.id:  
                        
                        #Check if the worker the player is trying to select can move
                        if not GameManager.get_game().can_worker_move(logic_tile.worker):
                            print(f"[DEBUG] This worker cannot move!")
                            self.show_worker_cannot_move_popup()
                        else:
                            print(f"[DEBUG] Worker FOUND on tile {position.x}-{position.y}. Selecting worker.")
                            self.selected_worker = logic_tile.worker
                            self.show_worker_selected_popup()
                            self.highlight_selected_worker()
                            self.current_phase = Phase.MOVE_WORKER
                            self.update_phase_info()
                            self.show_god_info()
                    else:
                        self.show_cannot_select_worker_popup()
                        print(f"[DEBUG] Cannot select other player's worker.")
                else:
                    print(
                        f"[DEBUG] No worker found on tile {position.x}-{position.y}.")

            case Phase.MOVE_WORKER:
                if self.selected_worker:
                    old_position = self.selected_worker.position

                    logic_tile = GameManager.current_game.get_tile(position)

                    if GameManager.current_game.validate_move_position(self.selected_worker, position):
                        print(f"[DEBUG] Moving worker to {position.x}-{position.y}")
                        GameManager.current_game.move_worker(self.selected_worker, position)
                        self.move_worker_visual(self.selected_worker, old_position, position)

                        god = GameManager.get_game().get_current_player().god
                        proceed_to_build = True
                        if god:
                            proceed_to_build = god.on_worker_moved(self.selected_worker, old_position, position, self)

                        if proceed_to_build:
                            if GameManager.current_game.check_if_winning_tile(position):
                                print("GAME WON")
                                SceneManager.change_scene(SceneID.GAME_OVER)

                            self.show_build_popup()
                            self.highlight_selected_worker()

                            #if moved worker cant build -> player loses
                            if not GameManager.current_game.can_worker_build(self.selected_worker):
                                print("GAME OVER")
                                #show a pop up
                                lost_player_id = GameManager.current_game.get_current_player().id
                                GameManager.get_game().end_turn()
                                self.show_loss_popup(
                                    player_id= lost_player_id,
                                    reason="Selected worker cannot build.",
                                    on_confirm=lambda: SceneManager.change_scene(SceneID.GAME_OVER)
                                )

                            self.current_phase = Phase.BUILD_STACK
                            self.update_phase_info()
                            self.show_god_info()
                        else:
                            self.highlight_selected_worker()
                            self.show_worker_selected_popup()

                    else:
                        self.show_invalid_movement_popup()

            case Phase.BUILD_STACK:
                print(f"[DEBUG] Building on tile at {position.x}-{position.y}")

                if self.selected_worker:
                    if GameManager.current_game.validate_build_position(self.selected_worker, position):
                        GameManager.current_game.add_stack(position)  # Update logic
                        logic_tile = GameManager.current_game.get_tile(position)
                        self.change_stack_visuals(position, logic_tile.stack_height)  # Update visuals

                        god = GameManager.get_game().get_current_player().god
                        next_turn = True
                        if god:
                            next_turn = god.on_stack_built(self.selected_worker, position, self)

                        if next_turn:
                            if GameManager.current_game.check_if_winning_tile(position):
                                print("GAME WON")
                                SceneManager.change_scene(SceneID.GAME_OVER)

                            self.show_build_popup()
                            self.highlight_selected_worker()
                            self.current_phase = Phase.SELECT_WORKER
                            self.selected_worker = None
                            self.update_phase_info()
                            self.show_god_info()
                            GameManager.get_game().end_turn()
                            self.highlight_current_players_workers()

                            #if next player cant move any worker -> player loses
                            if not GameManager.current_game.can_player_move(GameManager.current_game.get_current_player()):
                                print("GAME OVER")
                                lost_player_id = GameManager.current_game.get_current_player().id
                                GameManager.get_game().end_turn()
                                self.show_loss_popup(
                                    player_id=lost_player_id,
                                    reason="No available moves for any worker.",
                                    on_confirm=lambda: SceneManager.change_scene(SceneID.GAME_OVER) #will change for a multiplayer game
                                )
                            
                    else:
                        self.show_invalid_build_popup()

            case _:
                raise Exception("Invalid game phase.")
        # endregion

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]

    def change_stack_visuals(self, tile_position: Vector2I, stack_count: int):
        assert stack_count <= SettingManager.max_stacks_before_dome+1
        tile = self.get_tile(tile_position)

        for i in range(SettingManager.max_stacks_before_dome):
            if i <= stack_count-1:
                tile.canvas.itemconfigure(tile.stack_sprites[i], state=NORMAL)
            else:
                tile.canvas.itemconfigure(tile.stack_sprites[i], state=HIDDEN)

        tile.canvas.itemconfigure(tile.dome_sprite, state=(
            NORMAL if stack_count == SettingManager.max_stacks_before_dome + 1 else HIDDEN))

        # ! Note: this will still place a worker above a dome even if that is not allowed (this should not need to check)
        worker_centre_x = tile.scaled_tile_size.x // 2
        worker_centre_y = tile.scaled_tile_size.y - \
            tile.stack_grow_bottom_offset - tile.stack_height_px * stack_count

        tile.canvas.coords(
            tile.worker_sprite,
            worker_centre_x + WORKER_WIDTH_PX,
            worker_centre_y,
            worker_centre_x - WORKER_WIDTH_PX,
            worker_centre_y - WORKER_HEIGHT_PX)  # ! may need to scale with ui scaling

    def start_game(self, grid_size: Vector2I):
        assert grid_size.x > 0
        assert grid_size.y > 0
        self.size = grid_size
        self._grid = [[Tile(self.map_frame, Vector2I(x, y), lambda e, pos=Vector2I(
            x, y): self.__on_clicked_tile(pos, e)) for y in range(self.size.y)] for x in range(self.size.x)]

        # Randomly place workers
        self.place_random_workers()

    def place_random_workers(self):
        assert self._grid

        # Flatten the grid into a list of all tiles
        all_tiles = [tile for row in self._grid for tile in row]

        # Shuffle tiles
        random.shuffle(all_tiles)

        # --- Get all the workers ---
        workers = []
        for player in GameManager.current_game.players:
            workers.extend(player.workers)

        # --- Place each worker on a tile ---
        for worker, tile in zip(workers, all_tiles):
            tile.canvas.itemconfig(tile.worker_sprite, state=NORMAL)
            logic_tile = GameManager.current_game.get_tile(tile.position)
            logic_tile.worker = worker  # link the logic tile to the worker
            worker.position = tile.position  # update worker's position

    def move_worker_visual(self, worker: Worker, old_position: Vector2I, new_position: Vector2I):
        old_tile = self.get_tile(old_position)
        new_tile = self.get_tile(new_position)

        # Hide old tile sprite unconditionally
        old_tile.canvas.itemconfig(old_tile.worker_sprite, state=HIDDEN)

        # Show new tile sprite if logic says there's a worker
        logic_tile = GameManager.current_game.get_tile(new_position)
        if logic_tile.worker:
            new_tile.canvas.itemconfig(new_tile.worker_sprite, state=NORMAL)
        else:
            new_tile.canvas.itemconfig(new_tile.worker_sprite, state=HIDDEN)

    def cleanup(self):
        # TODO reset everything
        # TODO reset UI
        self.size = None
        self._grid = None
        self.selected_worker = None
        self.current_phase = Phase.SELECT_WORKER

    def show_player_turn_popup(self):
        current_player = GameManager.get_game().get_current_player()
        popup = Label(
            self.frame,
            text=f"Player {current_player.id}'s Turn!",
            font=("Helvetica", 18, "bold"),
            bg= POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1.5 second
        self.frame.after(1500, popup.destroy)

    def show_cannot_select_worker_popup(self):
        popup = Label(
            self.frame,
            text=f"Cannot select another player's worker!",
            font=("Helvetica", 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1.5 seconds
        self.frame.after(1500, popup.destroy)

    def show_worker_cannot_move_popup(self):
        popup = Label(
            self.frame,
            text=f"This worker cannot move! Please select another worker",
            font=("Helvetica", 18, "bold"),
            bg=POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1.5 seconds
        self.frame.after(1500, popup.destroy)

    def highlight_current_players_workers(self):
        assert self._grid

        # First remove any old highlights
        for row in self._grid:
            for tile in row:
                tile.canvas.itemconfig(tile.worker_sprite, outline="", width=1)

        # Highlight current player's workers
        current_player = GameManager.get_game().get_current_player()

        for worker in current_player.workers:
            tile = self.get_tile(worker.position)

            tile.canvas.itemconfig(
                tile.worker_sprite,
                outline="gold",
                width=5           
            )

    def highlight_selected_worker(self):
        # Remove old highlights first
        for row in self._grid:
            for tile in row:
                tile.canvas.itemconfig(tile.worker_sprite, outline="", width=1)

        if not self.selected_worker:
            return

        # Highlight the selected worker
        tile = self.get_tile(self.selected_worker.position)
        tile.canvas.itemconfig(
            tile.worker_sprite,
            outline="red",  # Use blue or any visible color
            width=5
        )

    def show_worker_selected_popup(self):
        popup = Label(
            self.frame,
            text=f"Worker Selected! Move your worker...",
            font=("Helvetica", 18, "bold"),
            bg= POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1.5 seconds
        self.frame.after(1500, popup.destroy)

    def show_build_popup(self):
        popup = Label(
            self.frame,
            text=f"Worker Moved! Click on an adjacent tile to build...",
            font=("Helvetica", 18, "bold"),
            bg= POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1.5 seconds
        self.frame.after(1500, popup.destroy)

    def show_invalid_movement_popup(self):
        popup = Label(
            self.frame,
            text=f"Worker cannot be moved here! Please try Again.",
            font=("Helvetica", 18, "bold"),
            bg= POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1 second
        self.frame.after(1000, popup.destroy)

    def show_invalid_build_popup(self):
        popup = Label(
            self.frame,
            text=f"Cannot build here! Please try Again.",
            font=("Helvetica", 18, "bold"),
            bg= POP_UP_COLOR,  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 1 second
        self.frame.after(1000, popup.destroy)
    
    def update_phase_info(self):
        current_player = GameManager.get_game().get_current_player()
        text = f"Player {current_player.id}'s Turn\n\n"

        match self.current_phase:
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
        popup = Toplevel(self.frame)
        popup.title("Player Eliminated")
        popup.geometry("450x250")
        popup.configure(bg="white")
        popup.grab_set()  # Prevent interaction with main window

        # Header
        title = Label(
            popup,
            text=f"Player {player_id} has been eliminated!",
            font=("Helvetica", 18, "bold"),
            fg="#FF0000",
            bg="white"
        )
        title.pack(pady=(20, 10))

        # Reason
        message = Label(
            popup,
            text=f"Reason: {reason}",
            font=("Helvetica", 14),
            bg="white",
            wraplength=400,
            justify="center"
        )
        message.pack(pady=10)

        # Continue Button
        continue_btn = Button(
            popup,
            text="Continue",
            font=("Helvetica", 12),
            command=lambda: self._handle_popup_close(popup, on_confirm)
        )
        continue_btn.pack(pady=20)

    def _handle_popup_close(self, popup: Toplevel, on_confirm: Callable[[], None]):
        popup.destroy()
        on_confirm() #could be used to continue game with remaining players or show winner


    def show_god_info(self):
        current_player = GameManager.get_game().get_current_player()
        text = f"God: {current_player.god.name}\n\n{current_player.god.description}"

        self.god_info_label.config(text=text)