from abc import ABC, abstractmethod

class God(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def on_worker_moved(self, worker, old_position, new_position, game_scene) -> bool:
        """Called after a worker has moved.
        Return True if turn should continue (go to build), or False to allow another move.
        """
        return True
    
    def on_stack_built(self, worker, position, game_scene) -> bool:
        """Called after a stack has been built.
        Return True if turn should continue (go to build), or False to allow another move.
        """
        return True

    @abstractmethod
    def modify_move(self, worker, board):
        """modify movement behavior."""
        pass

    @abstractmethod
    def modify_build(self, worker, board):
        """modify building behavior."""
        pass


class Artemis(God):
    def __init__(self):
        super().__init__(
            name="Artemis",
            description="Your Worker may move one additional time, but not back to its initial space."
        )
        self.first_move_done = False
        self.initial_position = None

    def on_worker_moved(self, worker, old_position, new_position, game_scene) -> bool:
        if not self.first_move_done:
            self.initial_position = old_position
            self.first_move_done = True
            game_scene.update_phase_info()
            return False  # Don't go to build phase yet
        else:
            # Disallow moving back to original space
            if new_position == self.initial_position:
                game_scene.show_invalid_movement_popup()
                return False
            # Now done, reset state
            return True

    def reset_turn_state(self):
        self.first_move_done = False
        self.initial_position = None

    def modify_move(self, worker, board):
        pass

    def modify_build(self, worker, board):
        pass


class Demeter(God):
    def __init__(self):
        super().__init__(
            name="Demeter",
            description="Your Worker may build one additional time, but not on the same space."
        )
        self.first_build_done = False
        self.build_position = None

    def on_stack_built(self, worker, position, game_scene) -> bool:
        if not self.first_build_done:
            self.build_position = position
            self.first_build_done = True
            game_scene.update_phase_info()
            return False  # Don't go to end turn yet
        else:
            # Disallow building back to original space
            if position == self.build_position:
                game_scene.show_invalid_build_popup()
                return False
            # Now done, reset state
            self.first_build_done = False
            self.build_position = None
            return True

    def modify_move(self, worker, board):
        pass

    def modify_build(self, worker, board):
        pass

    
