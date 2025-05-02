
from God import God
from Worker import Worker


class Player:
    # Keep count of number of players initialized (also their id)
    player_count = 0

    def __init__(self):
        self.god: God
        self.id = Player.player_count
        Player.player_count += 1 # * assign then increment
        self.workers: list[Worker] = [Worker(self.id), Worker(self.id)]

    def assign_god(self, god: God):
        self.god = god

    @staticmethod
    def reset_player_count():
        Player.player_count = 0
