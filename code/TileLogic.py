from MathLib.Vector import Vector2I

class LogicTile:
    def __init__(self, position: Vector2I):
        self.position = position
        self.stack_height = 0
        self.worker = None