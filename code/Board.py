from MathLib.Vector import Vector2I
from Tile import Tile
from Worker import Worker
from TileLogic import LogicTile


class Board:
    """
    The Board class represents functions that can be done to things on the board, which consists of a grid of tiles.
    Each tile can hold a stack of items and a worker.
    """

    def __init__(self, size: Vector2I):
        self.size = size

        # Creating a 2d grid of LogicTile objects
        self._grid: list[list[LogicTile]] = [[LogicTile(Vector2I(x, y)) for y in range(size.y)] for x in range(size.x)]

    # Do not think this is needed
    def get_tile(self, position: Vector2I):
        return self._grid[position.x][position.y]

    # Moves worker information from one tile to another
    def move_worker(self, worker: Worker, new_position: Vector2I):
        old_tile = self.get_tile(worker.position) if worker.position else None
        new_tile = self.get_tile(new_position)

        if old_tile:
            old_tile.worker = None
        new_tile.worker = worker
        worker.position = new_position

    # Adds a stack to the tile at the given position
    def add_stack(self, position: Vector2I):
        tile = self.get_tile(position)
        tile.stack_height += 1