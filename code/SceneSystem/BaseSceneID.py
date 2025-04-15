class BaseSceneID:
    ERR = -1


"""
Other option is to have This be a generic type inside SceneManager like so:
	BaseSceneID = TypeVar("BaseSceneID",bound=Enum)
	BaseSceneID = TypeVar("BaseSceneID",bound=int)
"""
