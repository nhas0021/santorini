from typing import List, Optional, Type
from ActionRecord import ActionRecord
from GameState import MapState
from God import God
from Player import Player
from enum import Enum, auto


class Phase(Enum):
    SELECT_WORKER = auto()
    MOVE_WORKER = auto()
    BUILD_STACK = auto()


class TurnManager:
    """
    Facilitates the process of turns/actions, storing and modifing the history of every move/action
    """

    def __init__(self, player_count: int, player_gods_preferences: List[Type[God]]) -> None:
        # * Generate players / assign
        self.players: list[Player] = []
        self._initialize_players(player_count, player_gods_preferences)
        self.current_player_index = 0
        self.current_phase: Phase

        self._turn_history: Optional[List[List[List[ActionRecord]]]] = None

    def _initialize_players(self, count: int, player_gods_preferences: List[Type[God]]):
        self.players.clear()
        Player.reset_player_count()

        for i in range(count):
            self.players.append(Player())
            # ? Initialise the instance from type and assign it
            self.players[i].assign_god(player_gods_preferences[i]())

    def get_turn(self, turn_number: int, player_index: int):
        assert self._turn_history
        return self._turn_history[turn_number][player_index]

    def increment_turn_record(self):
        if not self._turn_history:
            self._turn_history = [[] for _ in self.players]
        self._turn_history.append([[] for _ in self.players])

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def start_turn(self, game_state: MapState):
        assert self.get_current_player().god
        self.get_current_player().god.on_start_turn(game_state)

    def end_turn(self, game_state: MapState) -> None:
        assert self.get_current_player().god
        self.get_current_player().god.on_start_turn(game_state)
        # current_player = self.get_current_player()
        # if hasattr(current_player, "god") and current_player.god is not None:
        #     god = current_player.god
        #     if hasattr(god, "first_move_done"):
        #         god.first_move_done = False
        #     if hasattr(god, "initial_position"):
        #         god.initial_position = None

        # self.current_player_index = (
        #     self.current_player_index + 1) % len(self.players)
