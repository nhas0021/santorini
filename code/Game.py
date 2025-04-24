import tkinter as tk
from MathLib.Vector import Vector2I
from SceneID import SceneID
from Styles import *
from God import God
import random

from SceneSystem.Scene import Scene
from SceneSystem.SceneManager import SceneManager


class GameScene(Scene):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

#doesnt allow player naming yet (to be implemented in pre game scene)
class Player:
    player_count = 0 #Keep count of number of players initialized (also their id)

    def __init__(self):
        Player.player_count += 1
        self.god:God = None
        self.id = Player.player_count
        self.workers: list[Worker] = [Worker(self.id), Worker(self.id)]


    def assign_god(self, god: God):
        self.god = god

class Worker:
    def __init__(self, player_id: int):
        self.position: Vector2I = None  # ? Might not need
        self.player_id = player_id

class Tile:
    def __init__(self, position: Vector2I):
        self.position: Vector2I = position  # ? Might not need
        self.stack_height: int = 0
        self.worker: Worker = None

#changed MatchData to Game
class Game:
    """
    Stores all the information for a game/match.
    Implementation hides away the actual storage method/s.

    Note for hexagonal:
        - https://www.redblobgames.com/grids/hexagons/#map-storage
            - Python does not have 2D arrays - ONLY OPTIONS: Array of Arrays or Hash Table
    """

    #how do we want to initialize the gods? 1- Pass a list containing gods as a paramter of init
    #ensure number of players = number of gods
    def __init__(self, player_count: int, size: Vector2I, gods: list[God]):
        self._grid: list[list[Tile]] = [
            [Tile(Vector2I(x, y)) for x in range(size.y)] for y in range(size.x)]
        
        self.players: list[Player] = []
        self.initialize_players(player_count)
        self.gods: list[God] = gods

    def initialize_players(self, count):
        for x in range(count):
            self.players.append(Player())

    def assign_god_to_players(self):
        if len(self.gods) < len(self.players):
            print("Not enough gods for all players.")
            return

        random.shuffle(self.gods)

        for i in range(len(self.players)):
            god = self.gods[i]
            self.players[i].assign_god(god)

    def get_tile(self, position: Vector2I):
        return self._grid[position.x][position.y]
    
    def move_worker(self, worker: Worker, new_position: Vector2I):
        old_tile = self.get_tile(worker.position) if worker.position else None
        new_tile = self.get_tile(new_position)

        if old_tile:
            old_tile.worker = None

        new_tile.worker = worker
        worker.position = new_position

    def add_stack(self, position: Vector2I):
        tile = self.get_tile(position)
        tile.stack_height += 1