import random
from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame
from typing import Callable, List, Optional, Tuple
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
from Styles import *
from God import God
from Player import Player
from Tile import Tile
from TileLogic import LogicTile

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager
from GameManager import GameManager
from Worker import Worker

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

        self.current_phase = "select_worker" # can be select_worker, move_worker, build_stack

    def on_enter_scene(self):
        self.start_game(SettingManager.grid_size)

    def on_exit_scene(self):
        self.cleanup()

    # * Note that tkinter is not fully typed
    def __on_clicked_tile(self, position: Vector2I, e: Event) -> None:
        print(
            f"[DEBUG] Clicked on tile at {position.x}-{position.y}, Phase: {self.current_phase}")

        logic_tile = GameManager.current_game.get_tile(position)

        if self.current_phase == "select_worker":
            if logic_tile.worker:
                print(
                    f"[DEBUG] Worker FOUND on tile {position.x}-{position.y}. Selecting worker.")
                self.selected_worker = logic_tile.worker
                self.current_phase = "move_worker"
            else:
                print(
                    f"[DEBUG] No worker found on tile {position.x}-{position.y}.")

        elif self.current_phase == "move_worker":
            if self.selected_worker:
                print(
                    f"[DEBUG] Moving worker {self.selected_worker.player_id} to {position.x}-{position.y}")
                old_position = self.selected_worker.position

                GameManager.current_game.move_worker(self.selected_worker, position)
                self.move_worker_visual(self.selected_worker, old_position, position)

                self.current_phase = "build_stack"

        elif self.current_phase == "build_stack":
            print(f"[DEBUG] Building on tile at {position.x}-{position.y}")

            GameManager.current_game.add_stack(position)  # Update logic first

            logic_tile = GameManager.current_game.get_tile(position)  # Get logic tile
            # Use real level to update visuals
            self.change_stack_visuals(position, logic_tile.stack_height)

            self.current_phase = "select_worker"
            self.selected_worker = None

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]

    def change_stack_visuals(self, tile_position: Vector2I, stack_count: int):
        assert stack_count <= SettingManager.stacks_before_dome+1
        tile = self.get_tile(tile_position)

        for i in range(SettingManager.stacks_before_dome):
            if i <= stack_count-1:
                tile.canvas.itemconfigure(tile.stack_sprites[i], state=NORMAL)
            else:
                tile.canvas.itemconfigure(tile.stack_sprites[i], state=HIDDEN)

        worker_centre_x = tile.scaled_tile_size.x // 2
        worker_centre_y = tile.scaled_tile_size.y - \
            tile.stack_grow_bottom_offset - tile.stack_height * stack_count

        worker_width = 10
        worker_height = 40

        tile.canvas.coords(
            tile.worker_sprite,
            worker_centre_x + worker_width,
            worker_centre_y,
            worker_centre_x - worker_width,
            worker_centre_y - worker_height)

    def start_game(self, grid_size: Vector2I):
        assert grid_size.x > 0
        assert grid_size.y > 0
        self.size = grid_size
        self._grid = [[Tile(self.map_frame, Vector2I(x, y), lambda e, pos=Vector2I(x, y): self.__on_clicked_tile(pos, e)) for y in range(self.size.y)] for x in range(self.size.x)]

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
        old_tile.canvas.itemconfig(old_tile.worker_sprite, state="hidden")

        # Show new tile sprite if logic says there's a worker
        logic_tile = GameManager.current_game.get_tile(new_position)
        if logic_tile.worker:
            new_tile.canvas.itemconfig(new_tile.worker_sprite, state="normal")
        else:
            new_tile.canvas.itemconfig(new_tile.worker_sprite, state="hidden")

    def cleanup(self):
        # TODO reset everything
        # TODO reset UI
        self.size = None
        self._grid = None
