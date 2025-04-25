from MathLib.Vector import Vector2I


class Worker:
    def __init__(self, player_id: int):
        self.position: Vector2I = None  # ? Might not need
        self.player_id = player_id
