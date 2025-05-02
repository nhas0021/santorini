from typing import List, Optional, Type, cast
from God import God
from Player import Player
from TurnPhase import Phase


class TurnManager:
    """
    Facilitates the process of turns/actions, storing and modifing the history of every move/action
    """

    def __init__(self, player_count: int, player_gods_preferences: List[Optional[Type[God]]]) -> None:
        # * Generate players / assign
        self.players: list[Player] = []
        self._initialize_players(player_count, player_gods_preferences)
        self.current_player_index = 0
        self.current_phase: Phase = Phase.TURN_START

        self.winner: Optional[Player] = None
        self.losers: List[Player] = []

    def _initialize_players(self, count: int, player_gods_preferences: List[Optional[Type[God]]]):
        self.players.clear()
        Player.reset_player_count()

        for i in range(count):
            self.players.append(Player())
            # ? Initialise the instance from type and assign it
            assert player_gods_preferences[i]
            self.players[i].assign_god(
                cast(Type[God], player_gods_preferences[i])())

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def increment_player_turn(self):
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)

    # def start_turn(self, game_state: MapState):
    #     assert self.get_current_player().god
    #     self.get_current_player().god.on_start_turn(game_state)

    # def end_turn(self, game_state: MapState) -> None:
    #     assert self.get_current_player().god
    #     self.get_current_player().god.on_start_turn(game_state)
        # current_player = self.get_current_player()
        # if hasattr(current_player, "god") and current_player.god is not None:
        #     god = current_player.god
        #     if hasattr(god, "first_move_done"):
        #         god.first_move_done = False
        #     if hasattr(god, "initial_position"):
        #         god.initial_position = None

        # self.current_player_index = (
        #     self.current_player_index + 1) % len(self.players)
