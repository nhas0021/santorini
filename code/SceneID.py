from enum import Enum
from SceneSystem.BaseSceneID import BaseSceneID


class SceneID(BaseSceneID, Enum):
    TITLE = 1
    MAIN_MENU = 2
    GAME = 3
