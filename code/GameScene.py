import random
from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame, Label
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

    def on_enter_scene(self):
        self.start_game(SettingManager.grid_size)
        self.show_player_turn_popup()
        self.highlight_current_players_workers()

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
                if logic_tile.worker:
                    current_player = GameManager.get_game().get_current_player()
                    #Check if the worker the player is trying to select is the current player's worker
                    if logic_tile.worker.player_id == current_player.id:  
                        print(
                            f"[DEBUG] Worker FOUND on tile {position.x}-{position.y}. Selecting worker.")
                        self.selected_worker = logic_tile.worker
                        self.show_worker_selected_popup()
                        self.current_phase = Phase.MOVE_WORKER
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
                        print(
                            f"[DEBUG] Moving worker to {position.x}-{position.y}")
                        GameManager.current_game.move_worker(
                            self.selected_worker, position)
                        self.move_worker_visual(
                            self.selected_worker, old_position, position)
                        self.current_phase = Phase.BUILD_STACK
                        self.show_build_popup()

                # ! Note: "You win immediately if one of your workers moves from a lover level up to a level 3 tower"
                if GameManager.current_game.check_if_winning_tile(position):
                    print("GAME WON")  # TODO what happens after win
                    raise NotImplementedError

            case Phase.BUILD_STACK:
                print(f"[DEBUG] Building on tile at {position.x}-{position.y}")

                if self.selected_worker:
                    if GameManager.current_game.validate_build_position(self.selected_worker, position):
                        GameManager.current_game.add_stack(
                            position)  # Update logic
                        logic_tile = GameManager.current_game.get_tile(
                            position)
                        self.change_stack_visuals(
                            position, logic_tile.stack_height)  # Update visuals

                        GameManager.get_game().end_turn()
                        self.current_phase = Phase.SELECT_WORKER
                        self.selected_worker = None
                        self.show_player_turn_popup()
                        self.highlight_current_players_workers()

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

    def show_player_turn_popup(self):
        current_player = GameManager.get_game().get_current_player()
        popup = Label(
            self.frame,
            text=f"Player {current_player.id}'s Turn!",
            font=("Helvetica", 18, "bold"),
            bg="#FFFACD",  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 2 seconds
        self.frame.after(2000, popup.destroy)

    def show_cannot_select_worker_popup(self):
        popup = Label(
            self.frame,
            text=f"Cannot select another player's worker!",
            font=("Helvetica", 18, "bold"),
            bg="#FFFACD",  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 2 seconds
        self.frame.after(2000, popup.destroy)

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
                outline="gold",  # ✅ bright gold border
                width=5           # ✅ THICK border, very visible
            )

    def show_worker_selected_popup(self):
        popup = Label(
            self.frame,
            text=f"Worker Selected!",
            font=("Helvetica", 18, "bold"),
            bg="#FFFACD",  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 2 seconds
        self.frame.after(2000, popup.destroy)

    def show_build_popup(self):
        popup = Label(
            self.frame,
            text=f"Worker Moved! Click on an adjacent tile to build...",
            font=("Helvetica", 18, "bold"),
            bg="#FFFACD",  # light yellow
            fg="#333",
            relief="solid",
            bd=2,
            padx=10,
            pady=5
        )
        popup.place(relx=0.5, rely=0.05, anchor="n")

        # Auto-destroy popup after 2 seconds
        self.frame.after(2000, popup.destroy)





