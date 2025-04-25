from random import sample
from tkinter import NORMAL, HIDDEN, DISABLED, Canvas, Event, Misc, Tk, Frame
from typing import Callable, List, Optional, Tuple
from MathLib.Vector import Vector2I
from SceneID import SceneID
from SettingManager import SettingManager
from Styles import *
from God import God
from Player import Player
from Tile import Tile

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager
from GameManager import GameManager
from Worker import Worker


class GameScene(Scene):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)
        self.frame.config(background=WATER_COLOUR)

        self.size: Optional[Vector2I] = None
        # ! Note: Acess should be [x][y].
        self._grid: Optional[list[list[Tile]]] = None
        self.map_frame: Frame = Frame(
            self.frame, width=SettingManager.map_frame_size.x, height=SettingManager.map_frame_size.y, bg=DIRT_COLOUR, highlightthickness=15, highlightbackground=SAND_COLOUR)
        self.map_frame.place(relx=0.5, rely=0.5, anchor="center")

    def on_exit_scene(self):
        self.cleanup()

    # * Note that tkinter is not fully typed
    def __on_clicked_tile(self, position: Vector2I, e: Event) -> None:
        # TODO replace with game logic
        print(f"{position.x}-{position.y} | {e}")

    def get_tile(self, position: Vector2I) -> Tile:
        assert self._grid
        return self._grid[position.x][position.y]

    def change_stack_visuals(self, tile_position: Vector2I, stack_count: int):
        assert stack_count <= SettingManager.stacks_before_dome+1
        tile = self.get_tile(tile_position)

        for i in range(SettingManager.stacks_before_dome):
            if i <= stack_count-1:  # ? Active stacks
                tile.canvas.itemconfigure(
                    tile.stack_sprites[i], state=NORMAL)  # * show
            else:
                tile.canvas.itemconfigure(
                    tile.stack_sprites[i], state=HIDDEN)  # * hide

        # *Adjust worker pos (don't change visible state)
        tile.canvas.coords(
            tile.worker_sprite,
            tile.scaled_tile_size.x//2,
            tile.scaled_tile_size.y - tile.stack_grow_bottom_offset - tile.stack_height*stack_count)

    def start_game(self, grid_size: Vector2I):
        assert grid_size.x > 0
        assert grid_size.y > 0
        self.size = grid_size
        self._grid = [
            # * Generate tiles and give position data
            [Tile(self.map_frame,  Vector2I(x, y), lambda e, pos=Vector2I(x, y): self.__on_clicked_tile(pos, e)) for x in range(self.size.y)] for y in range(self.size.x)]

    def cleanup(self):
        # TODO reset everything
        # TODO reset UI
        self.size = None
        self._grid = None

    def move_worker(self, worker: Worker, new_position: Vector2I):
        old_tile = self.get_tile(worker.position) if worker.position else None
        new_tile = self.get_tile(new_position)

        if old_tile:
            old_tile.worker = None

        new_tile.worker = worker
        worker.position = new_position

    def add_stack(self, position: Vector2I):
        tile = self.get_tile(position)
        tile.stack_height += 1


