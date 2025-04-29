from random import sample
from typing import Literal, Optional
from MathLib.Vector import Vector2I
from SettingManager import SettingManager
from Player import Player
from Worker import Worker
from LogicTile import LogicTile


class Game:
    # ensure number of players = number of gods
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

    def check_unoccupied_space(self, position: Vector2I):
        """
        From rulesheet: Unoccupied Space: A space not containing a worker or dome.
        """
        if self.get_tile(position).stack_height >= SettingManager.max_stacks_before_dome+1:
            return False  # * dome check

        if self.get_tile(position).worker:
            return False  # * worker check

        return True

    def validate_move_position(self, worker: Worker, target_position: Vector2I, max_step_up: int = 1, max_step_down: int = None):
        # ! Ordered by speed for performance
        if worker.position == target_position:
            return False  # * cannot move to self

        if not target_position.is_adjacent(worker.position):
            return False  # * cannot move further than 1 tile (x)

        if not self.check_unoccupied_space(target_position):
            return False  # * cannot move onto occupied space

        if max_step_up and self.get_tile(worker.position).stack_height + max_step_up < self.get_tile(target_position).stack_height:
            return False  # * cannot move if too high (-1 = skip)
        if max_step_down and self.get_tile(worker.position).stack_height - max_step_down > self.get_tile(target_position).stack_height:
            return False  # * cannot move if too low (-1 = skip)

        return True

    def validate_build_position(self, worker: Worker, target_position: Vector2I):
        # ! Ordered by speed for performance
        if worker.position == target_position:
            return False  # * cannot buiild to self

        if not target_position.is_adjacent(worker.position):
            return False  # * cannot move further than 1 tile (x)

        if not self.check_unoccupied_space(target_position):
            return False  # * cannot build onto occupied space

        return True

    def check_if_winning_tile(self, position: Vector2I) -> Optional[Worker]:
        if (winning_worker := self.get_tile(position).worker) and (self.get_tile(position).stack_height == SettingManager.max_stacks_before_dome):
            return winning_worker
        return None

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
