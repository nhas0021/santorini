from typing import List
from Player import Player
from Worker import Worker

#seperate class to allow future modifications of turns affected by God Cards
class TurnManager:
    def __init__(self, players: List[Player]) -> None:
        self.players = players
        self.current_player_index = 0

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def end_turn(self) -> None:
        current_player = self.get_current_player()
        if hasattr(current_player, "god") and current_player.god is not None:
            god = current_player.god
            if hasattr(god, "first_move_done"):
                god.first_move_done = False
            if hasattr(god, "initial_position"):
                god.initial_position = None

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.selected_worker = None

