from typing import Dict, Optional

from SceneSystem.BaseSceneID import BaseSceneID
from SceneSystem.Scene import Scene


class SceneManager:
    _instance: Optional["SceneManager"] = None

    current_scene: Optional[Scene] = None
    scenes: Dict[BaseSceneID, Scene] = {}

    def __init__(self):
        if SceneManager._instance:
            raise Exception(
                "There must only be one instance of this singleton.")
        SceneManager._instance = self

    @staticmethod
    def register_scene(scene_id: BaseSceneID, scene: Scene) -> None:
        SceneManager.scenes[scene_id] = scene

    @staticmethod
    def change_scene(scene_id: BaseSceneID) -> None:
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
