from God import God
from MathLib.Vector import Vector2I
from Worker import Worker


class Blank(God):
    NAME = "None"
    DESCRIPTION = "No hero was chosen."


class Artemis(God):
    NAME = "Artemis"
    DESCRIPTION = "Your Worker may move one additional time, but not back to its initial space."

    def __init__(self):
        super().__init__()
        self.first_move_done = False
        self.initial_position = None

    def on_worker_moved(self, worker: Worker, old_position: Vector2I, new_position: Vector2I, game_scene) -> bool:
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


class Demeter(God):
    NAME = "Demeter"
    DESCRIPTION = "Your Worker may build one additional time, but not on the same space."

    def __init__(self):
        super().__init__()
        self.first_build_done = False
        self.build_position = None

    def on_stack_built(self, worker: Worker, position: Vector2I, game_scene) -> bool:
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
