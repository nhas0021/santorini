from MathLib.Vector import Vector2I


class SettingManager:
    # ~ Video
    screen_size: Vector2I
    # ~ Game Preferene
    player_count: int
    grid_size: Vector2I
    map_frame_size: Vector2I
    stacks_before_dome: int

    @staticmethod
    def load_defaults() -> None:
        SettingManager.screen_size = Vector2I(1920, 1080)

        SettingManager.player_count = 2
        SettingManager.grid_size = Vector2I(5, 5)
        SettingManager.map_frame_size = Vector2I(500, 500)
