from enum import Enum, auto


class Phase(Enum):
    TURN_START = auto()
    TURN_END = auto()
    SELECT_WORKER = auto()
    MOVE_WORKER = auto()
    BUILD_STACK = auto()
