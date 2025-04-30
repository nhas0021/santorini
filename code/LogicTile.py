from MathLib.Vector import Vector2I
from typing import Optional
from Worker import Worker

class LogicTile:
    def __init__(self, position: Vector2I):
        self.position = position
        self.stack_height:int = 0
        self.worker:Optional[Worker] = None