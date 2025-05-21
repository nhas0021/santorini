import json
from tkinter import filedialog
from typing import Optional
from MathLib.Vector import Vector2I
from TurnManager import TurnManager
from MapState import MapState
from Preferences import Preferences
from TurnPhase import Phase
from Player import Player
from Worker import Worker

class GameStorageManager:

    #to store game loaded from a file
    saved_game_data: Optional[dict] = None

    def save_game(turn_manager: TurnManager, map_state: MapState) -> bool:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Game As"
        )

        if not file_path:
            return False  # User cancelled

        game_state = GameStorageManager.extract_game_state(turn_manager, map_state)

        try:
            with open(file_path, "w") as f:
                json.dump(game_state, f, indent=4)
            print(f"[Saved] Game saved to {file_path}")
            return True
        except Exception as e:
            print(f"[Error] Could not save game: {e}")
            return False

    def extract_game_state(turn_manager: TurnManager, map_state: MapState):
        return {
            "players": [
                {
                    "id": player.id,
                    "god": player.god.NAME if player.god else None,
                    "workers": [[w.position.x, w.position.y] for w in player.workers]
                }
                for player in turn_manager.players
            ],
            "board": [
                [
                    map_state.get_tile(Vector2I(x, y)).stack_height
                    for y in range(map_state.size.y)
                ]
                for x in range(map_state.size.x)
            ],
            "current_turn_index": turn_manager.current_player_index,
            "game_phase": turn_manager.current_phase.name,
        }
    
    def load_into_scene(scene):
        """
        Rebuilds map_state and turn_manager inside the given GameScene using the saved JSON data.
        """

        data = GameStorageManager.saved_game_data

        def get_god_by_name(name: str):
            for god_cls in Preferences.gods_selectable:
                if god_cls.NAME == name:
                    return god_cls()

        # 1. Rebuild map state
        size_x = len(data["board"])
        size_y = len(data["board"][0])
        grid_size = Vector2I(size_x, size_y)
        scene.map_state = MapState(grid_size, Preferences.max_stacks_before_dome)
        scene.generate_tilemap_sprites(scene.map_state)

        for x in range(size_x):
            for y in range(size_y):
                scene.map_state.get_tile(Vector2I(x, y)).stack_height = data["board"][x][y]

        # 2. Rebuild TurnManager and players
        scene.turn_manager = TurnManager()
        scene.turn_manager.current_phase = Phase[data["game_phase"]]
        scene.turn_manager.current_player_index = data["current_turn_index"]

        for player_data in data["players"]:
            player = Player()
            player.workers.clear()
            player.id = player_data["id"]
            player.assign_god(get_god_by_name(player_data["god"]))

            for pos in player_data["workers"]:
                worker = Worker(player_data["id"])
                worker.position = Vector2I(*pos)
                player.workers.append(worker)
                scene.map_state.get_tile(worker.position).worker = worker

            scene.turn_manager.players.append(player)

        # 3. Update visuals
        for x in range(size_x):
            for y in range(size_y):
                scene.update_tile_visuals(Vector2I(x, y))

        # 4. Resume game flow
        scene.turn_manager.get_current_player().god.on_start_turn(scene)
        scene.turn_manager.get_current_player().god.on_start_current_phase(scene)
