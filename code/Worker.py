from MathLib.Vector import Vector2I


class Worker:
    def __init__(self, player_id: int):
        self.position: Vector2I = None  # ? Might not need
        self.player_id = player_id

    def move(self, new_position: Vector2I):
        """Move the worker to a new position."""
        pass

    def build(self, build_position: Vector2I):
        """Build at the specified position."""
        # Implement building logic here
        pass