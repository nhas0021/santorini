from typing import TypeVar, Generic, Dict, Optional
from typing import Self

SceneIDType = TypeVar("SceneIDType")


class SceneManager(Generic[SceneIDType]):
    _instance: Optional["SceneManager"] = None
    
    current_scene: Optional["Scene"] = None
    scenes: Dict[SceneIDType, "Scene"] = {} 

    def __init__(self):
        if SceneManager._instance:
            raise Exception(
                "There must only be one instance of this singleton.")
        SceneManager._instance = self

    @staticmethod
    def register_scene(scene_id: SceneIDType, scene: "Scene") -> None:
        SceneManager.scenes[scene_id] = scene

    @staticmethod
    def change_scene(scene_id: SceneIDType) -> None:
        if SceneManager.current_scene is None:
            print(
                f"Changing scene from N/A to {SceneManager.scenes[scene_id]}. (This may be an error)")
            SceneManager.current_scene = SceneManager.scenes[scene_id]
            SceneManager.current_scene.enable_scene()
            return

        print(
            f"Changing scene from {SceneManager.current_scene} to {SceneManager.scenes[scene_id]}.")
        SceneManager.current_scene.disable_scene()
        SceneManager.current_scene = SceneManager.scenes[scene_id]
        SceneManager.current_scene.enable_scene()
