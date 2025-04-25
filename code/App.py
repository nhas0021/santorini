import tkinter as tk

import Game
from SceneID import SceneID
from SettingManager import SettingManager
from SceneSystem.SceneManager import SceneManager
import Scenes

if __name__ == "__main__":

    # region Launch Args
    SettingManager()
    SettingManager.load_defaults()
    # ! load sys.argv
    # endregion

    # region Generate Window
    ROOT = tk.Tk()
    ROOT.title("DEMO")
    ROOT.geometry(
        f"{SettingManager.screen_size.x}x{SettingManager.screen_size.y}")

    SceneManager()  # ! Start it
    # endregion

    # region Generate and Register Scenes
    SceneManager.register_scene(SceneID.TITLE,  Scenes.Title(ROOT))
    SceneManager.register_scene(SceneID.MAIN_MENU,  Scenes.MainMenu(ROOT))

    SceneManager.register_scene(SceneID.PRE_GAME,  Scenes.PreGame(ROOT))

    SceneManager.register_scene(SceneID.PRE_GAME, Scenes.PreGame(ROOT))
    SceneManager.register_scene(SceneID.GAME, Game.GameScene(
        ROOT, SettingManager.map_frame_size))
    SceneManager.register_scene(
        SceneID.GOD_ASSIGNMENT, Scenes.GodAssignment(ROOT))

    SceneManager.register_scene(SceneID.RULEBOOK, Scenes.RuleBook(ROOT))
    # endregion

    # region Start Application
    # ! Make sure to show a screen on start
    SceneManager.change_scene(SceneID.TITLE)
    ROOT.mainloop()  # ! Start
    # endregion

"""
https://stackoverflow.com/a/76918213
"""
