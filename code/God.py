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

    def can_build_on(self, map_state, selected_worker, target_position, excluded = None) -> bool:
        # default behavior
        return map_state.validate_build_position(selected_worker, target_position, excluded)


    def clear_all_signals_in_phase(self, game_scene: "GameScene"):
        """Remove all the stored singals that were used this phase."""
        for tile in game_scene.map_state.for_all_tiles():
            for signal in self._signals_in_phase:
                if signal in tile.on_click_events:
                    tile.disconnect_on_click(signal)

    def after_selected_worker(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        """An overrideable (optional) event that is called after a valid tile with a worker is selected. """
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        self.initial_position = position
        self.selected_worker = game_scene.map_state.get_tile(position).worker

        # * can trigger show highlight visuals here

        print(
            f"[Notice] Worker selected @ {position} : {self.selected_worker}")

        assert self.selected_worker
        game_scene.highlight_selected_worker(self.selected_worker)
        game_scene.show_worker_selected_popup()
        game_scene.update_phase_info()

        game_scene.turn_manager.current_phase = Phase.MOVE_WORKER
        self.on_start_current_phase(game_scene)

    def after_selected_move_to(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        """An overrideable (optional) event that is called after a valid tile to move to is selected."""
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

        game_scene.show_build_popup()
        game_scene.highlight_selected_worker(self.selected_worker)
        game_scene.update_phase_info()

        print(
            f"[Notice] Worker {self.selected_worker} moved : {self.initial_position} >>> {self.moved_to}")

        # ! "The first player to move up to a level-3 tower wins!"
        if game_scene.map_state.check_if_winning_tile(self.moved_to):
            game_scene.turn_manager.winner = game_scene.turn_manager.get_current_player()
            game_scene.match_over()

        game_scene.turn_manager.current_phase = Phase.BUILD_STACK
        self.on_start_current_phase(game_scene)

    def after_selected_build(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        """An overrideable (optional) event that is called after a valid tile build on is selected."""
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        self.build_on = position

        game_scene.map_state.get_tile(
            self.build_on).stack_height += 1

        game_scene.update_tile_visuals(self.build_on)

        game_scene.update_phase_info()

        print(
            f"[Notice] Worker {self.selected_worker} built @ {self.build_on}")

        game_scene.turn_manager.current_phase = Phase.TURN_END
        self.on_start_current_phase(game_scene)

    def on_start_turn(self, game_scene: "GameScene"):
        """
        Variables should be reset at the start of a turn if needed, UI elements reset or triggered
        """
        print(f"{self.NAME} has started its turn.")

        self.selected_worker = None
        self.initial_position = None
        self.moved_to = None
        self.build_on = None

        game_scene.show_player_turn_popup()
        game_scene.highlight_current_players_workers()
        game_scene.update_phase_info()
        game_scene.show_god_info()

    def on_end_turn(self, game_scene: "GameScene"):
        """
        Variables should be cleaned up if needed, UI elements reset or triggered
        """
        print(f"{self.NAME} has ended its turn.")

    def on_start_current_phase(self, game_scene: "GameScene"):
        """
        Setup callbacks at the START of a phase - before anything else happens.

        Note: Custom heros can override this for their rules

        Note: Generally a phase setup will do the following:
            1) get all tiles
            2) check if they are valid to be selected during this phase
                a) if there are no valid tiles - stalemate/lose
            3) assign a callback event based on this choice
        """
        print(
            f"[Notice] Current phase is {game_scene.turn_manager.current_phase}")

        valid_move_exists = False
        while game_scene.turn_manager.get_current_player() in game_scene.turn_manager.losers:
            game_scene.turn_manager.increment_player_turn()  # * skip turn if already lost
            if game_scene.turn_manager.get_current_player() not in game_scene.turn_manager.losers and len(game_scene.turn_manager.losers) + 1 == len(game_scene.turn_manager.players):  # * last player standing
                game_scene.turn_manager.winner = game_scene.turn_manager.get_current_player()
                game_scene.match_over()
                return

        match game_scene.turn_manager.current_phase:
            case Phase.TURN_START:
                game_scene.enable_save_game_button(None)
                game_scene.turn_manager.current_phase = Phase.SELECT_WORKER
                self.on_start_current_phase(game_scene)
                valid_move_exists = True
            case Phase.TURN_END:
                # ? Turn over to next player
                game_scene.turn_manager.current_phase = Phase.TURN_START
                self.on_end_turn(game_scene)
                game_scene.turn_manager.increment_player_turn()
                game_scene.turn_manager.get_current_player().god.on_start_turn(game_scene)
                game_scene.turn_manager.get_current_player().god.on_start_current_phase(game_scene)
                valid_move_exists = True

            case Phase.SELECT_WORKER:
                # * for_all( if tile has worker add callback: after_selected_worker )
                for tile_state in game_scene.map_state.for_all_tiles():
                    if tile_state.worker and tile_state.worker.player_id == game_scene.turn_manager.current_player_index:
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_worker(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)
                        valid_move_exists = True
                game_scene.update_phase_info()
                game_scene.show_god_info()
    

            case Phase.MOVE_WORKER:
                game_scene.disable_save_game_button()
                exclude_moves = getattr(self, "tiles_moved_this_turn", None)
                for tile_state in game_scene.map_state.for_all_tiles():
                    assert self.selected_worker
                    # * valid move to
                    if exclude_moves is not None:
                        valid = game_scene.map_state.validate_move_position(
                            self.selected_worker, tile_state.position, excluded=exclude_moves)
                    else:
                        valid = game_scene.map_state.validate_move_position(
                            self.selected_worker, tile_state.position)
                    if valid:
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_move_to(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)
                        valid_move_exists = True
                    else:
                        pass  # attach warning signal
                game_scene.update_phase_info()
                game_scene.show_god_info()
            case Phase.BUILD_STACK:
                exclude_builds = getattr(
                    self, "tiles_built_on_this_turn", None)
                for tile_state in game_scene.map_state.for_all_tiles():
                    assert self.selected_worker
                    if exclude_builds is not None:
                        valid = self.can_build_on(game_scene.map_state, self.selected_worker, tile_state.position, excluded=exclude_builds)
                    else:
                        valid = self.can_build_on(game_scene.map_state, self.selected_worker, tile_state.position)
                    if valid:
                        signal: Callable[[Event[Canvas], Vector2I], None] = lambda _event, _position: self.after_selected_build(
                            game_scene, _event, _position)
                        tile_state.connect_on_click(signal)
                        self._signals_in_phase.append(signal)
                        valid_move_exists = True
                game_scene.update_phase_info()
                game_scene.show_god_info()
        if not valid_move_exists:
            print("[Notice] Player lost, no valid actions (stalemate).")
            game_scene.turn_manager.losers.append(
                game_scene.turn_manager.get_current_player())
            game_scene.turn_manager.increment_player_turn()

            game_scene.turn_manager.current_phase = Phase.TURN_END
            self.on_start_current_phase(game_scene)
            return


class Blank(God):
    NAME = "None"
    DESCRIPTION = "No hero was chosen."


class Artemis(God):
    NAME = "Artemis"
    DESCRIPTION = "Your Worker may move one additional time, but not back to its initial space."

    def __init__(self):
        super().__init__()
        self.moved_to_second: Optional[Vector2I] = None
        self.tiles_moved_this_turn: list[Vector2I] = []

    def after_selected_move_to(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        if not self.moved_to:
            # * regular
            self.moved_to = position
            self.tiles_moved_this_turn.append(position)
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
                f"[Notice] Worker {self.selected_worker} moved : {self.initial_position} >>> {self.moved_to}")

            # ! "The first player to move up to a level-3 tower wins!"
            if game_scene.map_state.check_if_winning_tile(self.selected_worker.position):
                game_scene.turn_manager.winner = game_scene.turn_manager.get_current_player()
                game_scene.match_over()

            # * show skip move button: on click change skip game phase
            def _skip_action():
                game_scene.disable_skip_button()
                self.clear_all_signals_in_phase(game_scene)
                game_scene.turn_manager.current_phase = Phase.BUILD_STACK
                self.on_start_current_phase(game_scene)
            game_scene.enable_skip_button(_skip_action)
            game_scene.turn_manager.current_phase = Phase.MOVE_WORKER
            self.on_start_current_phase(game_scene)
        else:
            # * ability (2nd move)
            game_scene.disable_skip_button()  # ? was not used, remove
            self.moved_to_second = position
            self.tiles_moved_this_turn.append(position)
            assert self.moved_to_second

            assert game_scene.map_state.get_tile(
                self.moved_to).worker == self.selected_worker, "Worker unexpectedly replaced."
            game_scene.map_state.get_tile(self.moved_to).worker = None
            game_scene.map_state.get_tile(
                self.moved_to_second).worker = self.selected_worker
            assert self.selected_worker
            self.selected_worker.position = self.moved_to_second

            game_scene.update_tile_visuals(self.moved_to)
            game_scene.update_tile_visuals(self.moved_to_second)

            print(
                f"[Notice] Worker {self.selected_worker} moved (again): {self.moved_to} >>> {self.moved_to_second}")

            # ! "The first player to move up to a level-3 tower wins!"
            if game_scene.map_state.check_if_winning_tile(self.selected_worker.position):
                game_scene.turn_manager.winner = game_scene.turn_manager.get_current_player()
                game_scene.match_over()

            game_scene.turn_manager.current_phase = Phase.BUILD_STACK
            self.on_start_current_phase(game_scene)

    def on_start_turn(self,  game_scene: "GameScene"):
        super().on_start_turn(game_scene)
        self.moved_to_second = None
        self.tiles_moved_this_turn = []


class Demeter(God):
    NAME = "Demeter"
    DESCRIPTION = "Your Worker may build one additional time, but not on the same space."

    def __init__(self):
        super().__init__()
        self.build_on_second: Optional[Vector2I] = None
        self.tiles_built_on_this_turn: list[Vector2I] = []

    def on_start_turn(self,  game_scene: "GameScene"):
        super().on_start_turn(game_scene)
        self.build_on_second = None
        self.tiles_built_on_this_turn = []

    def after_selected_build(self, game_scene: "GameScene", event: "Event[Canvas]", position: Vector2I):
        # * for_all remove callback: after_selected_worker
        self.clear_all_signals_in_phase(game_scene)

        if not self.build_on:
            # * first build
            self.build_on = position
            self.tiles_built_on_this_turn.append(position)

            game_scene.map_state.get_tile(
                self.build_on).stack_height += 1

            game_scene.update_tile_visuals(self.build_on)

            print(
                f"[Notice] Worker {self.selected_worker} built @ {self.build_on}")

            # * show skip move button: on click change skip game phase
            def _skip_action():
                game_scene.disable_skip_button()
                self.clear_all_signals_in_phase(game_scene)
                game_scene.turn_manager.current_phase = Phase.TURN_END
                self.on_start_current_phase(game_scene)
            game_scene.enable_skip_button(_skip_action)
            game_scene.turn_manager.current_phase = Phase.BUILD_STACK
            self.on_start_current_phase(game_scene)

        else:
            # * second (ability) build
            game_scene.disable_skip_button()  # ? was not used, remove
            self.build_on_second = position
            self.tiles_built_on_this_turn.append(position)

            game_scene.map_state.get_tile(
                self.build_on_second).stack_height += 1

            game_scene.update_tile_visuals(self.build_on_second)

            print(
                f"[Notice] Worker {self.selected_worker} built (again) @ {self.build_on_second}")

            game_scene.turn_manager.current_phase = Phase.TURN_END
            self.on_start_current_phase(game_scene)

class Zeus(God):
    NAME = "Zeus"
    DESCRIPTION = "Your Worker may build a block under itself."

    def can_build_on(self, map_state, worker, target_position, excluded=None):
        if target_position == worker.position:
            return True #cannot build dome under worker as player would have already won in that case
        return super().can_build_on(map_state, worker, target_position, excluded)
