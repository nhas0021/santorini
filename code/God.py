from GameState import MapState
from MathLib.Vector import Vector2I
from Worker import Worker


class God:
    NAME: str = "PLACEHOLDER NAME"
    """Override this."""
    DESCRIPTION: str = "PLACEHOLDER DESCRIPTION"
    """Override this."""

    def on_start_turn(self,  game_state: MapState):
        """
        Variables should be cleaned up if needed, UI elements reset or triggered
        """

    def on_end_turn(self,  game_state: MapState):
        """
        Variables should be cleaned up if needed, UI elements reset or triggered
        """

    def on_worker_moved(self, worker: Worker, old_position: Vector2I, new_position: Vector2I, game_scene) -> bool:
        """Called after a worker has moved.
        Return True if turn should continue (go to build), or False to allow another move.
        """
        return True

    def on_stack_built(self, worker: Worker, position: Vector2I, game_scene) -> bool:
        """Called after a stack has been built.
        Return True if turn should continue (go to build), or False to allow another move.
        """
        return True
