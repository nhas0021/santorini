import tkinter as tk

from SceneID import SceneID
from Preferences import Preferences
from SceneSystem.SceneManager import SceneManager
import Scenes
import GameScene

if __name__ == "__main__":
    Preferences()
    # region Launch Args
    Preferences.load_defaults()
    # ! load sys.argv if needed
    # endregion

    # region Generate Window
    ROOT = tk.Tk()
    ROOT.title("Santorini")
    ROOT.geometry(
        f"{Preferences.screen_size.x}x{Preferences.screen_size.y}")

    SceneManager()  # ! Start it
    # endregion

    # region Generate and Register Scenes
    SceneManager.register_scene(SceneID.TITLE,  Scenes.Title(ROOT))
    SceneManager.register_scene(SceneID.MAIN_MENU,  Scenes.MainMenu(ROOT))
    SceneManager.register_scene(SceneID.PRE_GAME,  Scenes.PreGame(ROOT))
    SceneManager.register_scene(SceneID.GAME, GameScene.GameScene(ROOT))
    SceneManager.register_scene(SceneID.GOD_ASSIGNMENT, Scenes.GodAssignment(ROOT))
    SceneManager.register_scene(SceneID.RULEBOOK, Scenes.RuleBook(ROOT))
    # endregion

    # region Start Application
    # ! Make sure to show a screen on start
    SceneManager.change_scene(SceneID.TITLE)
    ROOT.mainloop()  # ! Start
    # endregion

