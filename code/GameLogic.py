from random import sample
from MathLib.Vector import Vector2I
from SettingManager import SettingManager
from Player import Player
from Worker import Worker
from LogicTile import LogicTile

class Game:
    #ensure number of players = number of gods
    def __init__(self, player_count: int, size: Vector2I):
        self.size = size
        self._grid: list[list[LogicTile]] = [
            [LogicTile(Vector2I(x, y)) for y in range(size.y)]
            for x in range(size.x)
        ]
        self.players: list[Player] = []
        self.initialize_players(player_count)

    def initialize_players(self, count: int):
        self.players.clear()
        Player.reset_player_count()

        for _ in range(count):
            self.players.append(Player())

    def assign_gods_random_from_list(self):
        if len(SettingManager.selectable_gods) < len(self.players):
            print("Not enough unique gods for all players.")
            return

        rng_selected = sample(
            # ? can also add weights
            SettingManager.selectable_gods, len(self.players))

        for (p, g) in zip(self.players, rng_selected):  # assign
            p.assign_god(g)

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
    
