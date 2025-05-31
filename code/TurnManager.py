from typing import List, Optional, Type, cast
from God import God
from Player import Player
from TurnPhase import Phase
from Preferences import Preferences
from random import sample


class TurnManager:
    """
    Facilitates the process of turns/actions, storing and modifing the history of every move/action
    """

    def __init__(self) -> None:
        # * Generate players / assign
        self.players: list[Player] = []
        self.current_player_index = 0
        self.current_phase: Phase = Phase.TURN_START
        self.winner: Optional[Player] = None
        self.losers: List[Player] = []
        self.total_turns_played = 0 #reset when loaded from a saved game


    def initialize_players(self, count: int, player_gods_preferences: List[Optional[Type[God]]]):
        """Initializes player instances and assigns each a god based on preferences."""
        self.players.clear()
        Player.reset_player_count()

        for i in range(count):
            self.players.append(Player())
            # ? Initialise the instance from type and assign it
            assert player_gods_preferences[i]
            self.players[i].assign_god(
                cast(Type[God], player_gods_preferences[i])())

    def get_current_player(self) -> Player:
        """Returns the player whose turn it currently is."""
        return self.players[self.current_player_index]

    def increment_player_turn(self):
        """Advances the turn to the next player in a circular manner."""
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)
        
    def randomize_gods(self):
        """Randomly reassigns new god powers to all players from the selectable list."""
        print("[Randomize Gods] Reassigning gods...")

        assert Preferences.player_count <= len(Preferences.gods_selectable), \
            "Not enough gods for the number of players."

        Preferences.gods_preferences = sample(
            Preferences.gods_selectable, Preferences.player_count
        )

        for i, player in enumerate(self.players):
            god_cls = Preferences.gods_preferences[i]
            player.god = god_cls()
            print(f"Player {i + 1} is now {player.god.NAME}")

    #prevents circular import error in God.py
    def check_reassignment_preferences(self):
        """Checks if periodic god reassignment is enabled in preferences."""
        return Preferences.reassign_gods_during_game