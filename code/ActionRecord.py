from dataclasses import dataclass
from MathLib.Vector import Vector2I
from Worker import Worker


@dataclass
class ActionRecord:
    worker: Worker


@dataclass
class ActionSelectWorker(ActionRecord):
    pass


@dataclass
class ActionMove(ActionRecord):
    move_from: Vector2I
    move_to: Vector2I


@dataclass
class ActionBuild(ActionRecord):
    build_position: Vector2I
    is_built_dome: bool