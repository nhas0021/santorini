from MathLib.Vector import Vector2I
from Tile import Tile
from Worker import Worker

class Board:
    """
    The Board class represents functions that can be done to things on the board, which consists of a grid of tiles.
    Each tile can hold a stack of items and a worker.
    """
    def __init__(self, size: Vector2I):
        self._grid: list[list[Tile]]

    def get_tile(self, position: Vector2I):
        return self._grid[position.x][position.y]

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