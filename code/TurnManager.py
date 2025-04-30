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
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

