import tkinter as tk

import Game
from SceneID import SceneID
from SettingManager import SettingManager
from SceneSystem.SceneManager import SceneManager
import Scenes

if __name__ == "__main__":

    # region Launch Args
    # sys.argv

    screen_width: int = 1280
    screen_height: int = 720
    # endregion

    # region Generate Window
    ROOT = tk.Tk()
    ROOT.title("DEMO")
    ROOT.geometry(f"{screen_width}x{screen_height}")

    SettingManager()  # ! Start it
    SceneManager()  # ! Start it
    # endregion

    # region Generate and Register Scenes
    SceneManager.register_scene(SceneID.TITLE,  Scenes.Title(
        ROOT))
    SceneManager.register_scene(SceneID.MAIN_MENU,  Scenes.MainMenu(
        ROOT))

    SceneManager.register_scene(SceneID.PRE_GAME, Scenes.CharacterSelect(ROOT))
    SceneManager.register_scene(SceneID.GAME, Game.GameScene(
        ROOT, SettingManager.map_frame_size))
    # endregion

    # region Start Application
    # ! Make sure to show a screen on start
    SceneManager.change_scene(SceneID.TITLE)
    ROOT.mainloop()  # ! Start
    # endregion

"""
https://stackoverflow.com/a/76918213
"""
