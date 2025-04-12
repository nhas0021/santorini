import tkinter as tk

from SceneID import SceneID
from SceneSystem.SceneManager import SceneManager
import Scenes

# region Consts


def DEFAULT_CALLBACK():
    print("OVERRIDE THIS")
# endregion


# region Launch Args
screen_width: int = 1280
screen_height: int = 720
# endregion

# region Generate Window
ROOT = tk.Tk()
ROOT.title("DEMO")
ROOT.geometry(f"{screen_width}x{screen_height}")

SceneManager()  # ! Start it
# endregion


# region Generate and Register Scenes
SceneManager.register_scene(SceneID.TITLE,  Scenes.Title(
    ROOT))
SceneManager.register_scene(SceneID.MAIN_MENU,  Scenes.MainMenu(
    ROOT))

# endregion

# region Start Application
SceneManager.change_scene(SceneID.TITLE)  # ! Make sure to show a screen on start
ROOT.mainloop()  # ! Start
# endregion
