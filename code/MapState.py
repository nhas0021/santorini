from typing import Optional
from MathLib.Vector import Vector2I
from Worker import Worker
from TileState import TileState


class MapState:
    def __init__(self, size: Vector2I, max_stacks_before_dome: int):
        # ! Save match settings to this instance of a game (usually this is loaded from preferences)
        self.max_stacks_before_dome = max_stacks_before_dome
        self.size = size

        # * Generate map state
        self._map_state: list[list[TileState]] = [
            [TileState(Vector2I(x, y)) for y in range(size.y)]
            for x in range(size.x)
        ]

    def get_tile(self, position: Vector2I):
        return self._map_state[position.x][position.y]

    def for_all_tiles(self):
        """ A special accesssor for iterating over all items. """
        for row in self._map_state:
            for item in row:
                yield item

    def check_unoccupied_space(self, position: Vector2I):
        """
        From rulesheet: Unoccupied Space: A space not containing a worker or dome.
        """
        if self.get_tile(position).stack_height >= self.max_stacks_before_dome+1:
            return False  # * dome check

        if self.get_tile(position).worker:
            return False  # * worker check

        return True

    def validate_move_position(self, worker: Worker, target_position: Vector2I, max_step_up: int = 1, max_step_down: Optional[int] = None, excluded: Optional[list[Vector2I]] = None):
        if excluded and target_position in excluded:
            return False
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

    def validate_build_position(self, worker: Worker, target_position: Vector2I, excluded: Optional[list[Vector2I]] = None):
        if excluded and target_position in excluded:
            return False
        # ! Ordered by speed for performance
        if worker.position == target_position:
            return False  # * cannot buiild to self

        if not target_position.is_adjacent(worker.position):
            return False  # * cannot move further than 1 tile (x)

        if not self.check_unoccupied_space(target_position):
            return False  # * cannot build onto occupied space

        return True

    def check_if_winning_tile(self, position: Vector2I) -> Optional[Worker]:
        if (winning_worker := self.get_tile(position).worker) and (self.get_tile(position).stack_height == self.max_stacks_before_dome):
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

    # def get_current_player(self) -> Player:
    #     return self.turn_manager.get_current_player()

    def end_turn(self) -> None:
        # TODO self.turn_manager.end_turn()
        pass

    def can_worker_move(self, worker: Worker) -> bool:
        for pos in worker.position.get_adjacent_positions(self.size):
            if self.validate_move_position(worker, pos):
                return True
        return False

    def can_worker_build(self, worker: Worker) -> bool:
        for pos in worker.position.get_adjacent_positions(self.size):
            if self.validate_build_position(worker, pos):
                return True
        return False

    # def can_player_move(self, player: Player) -> bool:
    #     return any(self.can_worker_move(w) for w in player.workers)
