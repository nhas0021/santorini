import json
from tkinter import filedialog
from MathLib.Vector import Vector2I
from TurnManager import TurnManager
from MapState import MapState

class GameSaver:
    def __init__(self, turn_manager: TurnManager, map_state: MapState):
        self.turn_manager = turn_manager
        self.map_state = map_state

    def save_game(self) -> bool:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Game As"
        )

        if not file_path:
            return False  # User cancelled

        game_state = self.extract_game_state()

        try:
            with open(file_path, "w") as f:
                json.dump(game_state, f, indent=4)
            print(f"[Saved] Game saved to {file_path}")
            return True
        except Exception as e:
            print(f"[Error] Could not save game: {e}")
            return False

    def extract_game_state(self):
        return {
            "players": [
                {
                    "id": player.id,
                    "god": player.god.NAME if player.god else None,
                    "workers": [[w.position.x, w.position.y] for w in player.workers]
                }
                for player in self.turn_manager.players
            ],
            "board": [
                [
                    self.map_state.get_tile(Vector2I(x, y)).stack_height
                    for y in range(self.map_state.size.y)
                ]
                for x in range(self.map_state.size.x)
            ],
            "current_turn_index": self.turn_manager.current_player_index,
            "game_phase": self.turn_manager.current_phase.name,
        }
