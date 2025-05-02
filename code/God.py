from tkinter import Canvas, Event
from typing import TYPE_CHECKING, Callable, List, Optional
from MathLib.Vector import Vector2I
from TurnPhase import Phase
from Worker import Worker
if TYPE_CHECKING:
    from GameScene import GameScene


class God:
    NAME: str = "PLACEHOLDER NAME"
    """Override this."""
    DESCRIPTION: str = "PLACEHOLDER DESCRIPTION"
    """Override this."""

    def __init__(self):
        self._signals_in_phase: List[Callable[[
            Event[Canvas], Vector2I], None]] = []

        self.selected_worker: Optional[Worker] = None
        self.initial_position: Optional[Vector2I] = None
        self.moved_to: Optional[Vector2I] = None
        self.build_on: Optional[Vector2I] = None

    def clear_all_signals_in_phase(self,  game_scene: "GameScene"):
        for tile in game_scene.map_state.for_all_tiles():
            for signal in self._signals_in_phase:
                if signal in tile.on_click_events:
                    tile.disconnect_on_click(signal)

    def after_selected_worker(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        self.initial_position = position
        self.selected_worker = game_scene.map_state.get_tile(position).worker

        # TODO show highlight visuals

        print(
            f"[Notice] Worker selected @ {position} : {self.selected_worker}")

        game_scene.turn_manager.current_phase = Phase.MOVE_WORKER
        self.on_start_current_phase(game_scene)

    def after_selected_move_to(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        self.moved_to = position
        assert self.initial_position
        assert self.moved_to

        assert game_scene.map_state.get_tile(
            self.initial_position).worker == self.selected_worker, "Worker unexpectedly replaced."
        game_scene.map_state.get_tile(self.initial_position).worker = None
        game_scene.map_state.get_tile(
            self.moved_to).worker = self.selected_worker
        assert self.selected_worker
        self.selected_worker.position = self.moved_to

        game_scene.update_tile_visuals(self.initial_position)
        game_scene.update_tile_visuals(self.moved_to)

        print(
            f"[Notice] Worker {self.selected_worker} moved : {self.initial_position} >> {self.moved_to}")

        game_scene.turn_manager.current_phase = Phase.BUILD_STACK
        self.on_start_current_phase(game_scene)

    def after_selected_build(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        self.build_on = position

        game_scene.map_state.get_tile(
            self.build_on).stack_height += 1

        game_scene.update_tile_visuals(self.build_on)

        print(
            f"[Notice] Worker {self.selected_worker} built @ {self.build_on}")

        game_scene.turn_manager.current_phase = Phase.TURN_END
        self.on_start_current_phase(game_scene)

    # def on_worker_moved(self, worker: Worker, old_position: Vector2I, new_position: Vector2I, game_scene) -> bool:
    #     """Called after a worker has moved.
    #     Return True if turn should continue (go to build), or False to allow another move.
    #     """
    #     return True

    # def on_stack_built(self, worker: Worker, position: Vector2I, game_scene) -> bool:
    #     """Called after a stack has been built.
    #     Return True if turn should continue (go to build), or False to allow another move.
    #     """
    #     return True

    def on_start_turn(self, game_scene: "GameScene"):
        """
        Variables should be initialised if needed, UI elements reset or triggered
        """
        print(f"{self.NAME} has started its turn.")

        self.on_start_current_phase(game_scene)

    def on_end_turn(self, game_scene: "GameScene"):
        """
        Variables should be cleaned up if needed, UI elements reset or triggered
        """
        print(f"{self.NAME} has ended its turn.")

        self.selected_worker = None
        self.moved_to = None
        self.build_on = None

        self.on_start_current_phase(game_scene)

    def on_start_current_phase(self, game_scene: "GameScene"):
        """
        Setup callbacks at the START of a phase - before anything else happens.

        Note: Custom heros can override this for their rules

        Note: Generally a phase setup will do the following:
            1) get all tiles
            2) check if they are valid to be selected during this phase
            3) assign a callback event based on this choice
        """
        print(
            f"[Notice] Current scene is {game_scene.turn_manager.current_phase}")
        match game_scene.turn_manager.current_phase:
            case Phase.TURN_START:
                game_scene.turn_manager.current_phase = Phase.SELECT_WORKER
                self.on_start_current_phase(game_scene)
            case Phase.TURN_END:
                # ? Turn over to next player
                game_scene.turn_manager.current_phase = Phase.TURN_START
                game_scene.turn_manager.increment_player_turn()
                self.on_end_turn(game_scene)

            case Phase.SELECT_WORKER:
                # * for_all( if tile has worker add callback: after_selected_worker )
                for tile_state in game_scene.map_state.for_all_tiles():
                    if tile_state.worker and tile_state.worker.player_id == game_scene.turn_manager.current_player_index:
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_worker(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)

            case Phase.MOVE_WORKER:
                for tile_state in game_scene.map_state.for_all_tiles():
                    assert self.selected_worker
                    # * valid move to
                    if game_scene.map_state.validate_move_position(self.selected_worker, tile_state.position):
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_move_to(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)
                    else:
                        pass  # attach warning signal
            case Phase.BUILD_STACK:
                for tile_state in game_scene.map_state.for_all_tiles():
                    assert self.selected_worker
                    if game_scene.map_state.validate_build_position(self.selected_worker, tile_state.position):
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_build(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)


class Blank(God):
    NAME = "None"
    DESCRIPTION = "No hero was chosen."


class Artemis(God):
    NAME = "Artemis"
    DESCRIPTION = "Your Worker may move one additional time, but not back to its initial space."

    def __init__(self):
        super().__init__()
        # self.first_move_done = False
        # self.initial_position = None

    # def on_worker_moved(self, worker: Worker, old_position: Vector2I, new_position: Vector2I, game_scene) -> bool:
    #     if not self.first_move_done:
    #         self.initial_position = old_position
    #         self.first_move_done = True
    #         game_scene.update_phase_info()
    #         return False  # Don't go to build phase yet
    #     else:
    #         # Disallow moving back to original space
    #         if new_position == self.initial_position:
    #             game_scene.show_invalid_movement_popup()
    #             return False
    #         # Now done, reset state
    #         return True

    def on_end_turn(self,  game_scene: "GameScene"):
        super().on_end_turn(game_scene)
        self.first_move_done = False
        self.initial_position = None


class Demeter(God):
    NAME = "Demeter"
    DESCRIPTION = "Your Worker may build one additional time, but not on the same space."

    def __init__(self):
        super().__init__()
        # self.first_build_done = False
        # self.build_position = None

    # def on_stack_built(self, worker: Worker, position: Vector2I, game_scene) -> bool:
    #     if not self.first_build_done:
    #         self.build_position = position
    #         self.first_build_done = True
    #         game_scene.update_phase_info()
    #         return False  # Don't go to end turn yet
    #     else:
    #         # Disallow building back to original space
    #         if position == self.build_position:
    #             game_scene.show_invalid_build_popup()
    #             return False
    #         # Now done, reset state
    #         self.first_build_done = False
    #         self.build_position = None
    #         return True
