from typing import Dict, Optional

from SceneSystem.BaseSceneID import BaseSceneID
from SceneSystem.Scene import Scene


class SceneManager:
    """
    Motivation:
    - Isolation of data:
        - Allows for better encapusulation
        - Hiding the various objects (scope-wise) within the scene (buttons and labels) from other scenes
    - Standardised & Clean Transitions
        - Allows for multiple people to work on different parts of the game without interference
        - Clean way to change scenes

    """
    current_scene: Optional[Scene] = None
    scenes: Dict[BaseSceneID, Scene] = {}

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
        SceneManager.current_scene.on_exit_scene()
        SceneManager.current_scene.disable_scene()
        SceneManager.current_scene = SceneManager.scenes[scene_id]
        SceneManager.current_scene.on_enter_scene()
        SceneManager.current_scene.enable_scene()
