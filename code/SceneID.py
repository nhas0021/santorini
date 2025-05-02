from enum import Enum
from SceneSystem.BaseSceneID import BaseSceneID


class SceneID(BaseSceneID, Enum):
    """Our custom scenes"""
    TITLE = 1
    MAIN_MENU = 2
    TUTORIAL = 3
    RULEBOOK = 4
    PRE_GAME = 5
    GAME = 6
    SETTINGS = 7
    GOD_ASSIGNMENT = 8
