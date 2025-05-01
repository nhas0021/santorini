from dataclasses import dataclass
from tkinter import Event, Misc
from MathLib.Vector import Vector2I
from typing import Any, Callable, List, Optional
from Worker import Worker


@dataclass
class TileState:
    def __init__(self, position: Vector2I):
        self.position = position
        self.stack_height: int = 0
        self.worker: Optional[Worker] = None
        self._on_click_events: List[Callable[[Vector2I, Event], None]]

    def subscribe_on_click(self, event: Callable[[Vector2I, Event], None]):
        if event in self._on_click_events:
            print("[Warning] Event already subscribed.")
            return
        self._on_click_events.append(event)

    def unsubscribe_on_click(self, event: Callable[[Vector2I, Event], None]):
        if not event in self._on_click_events:
            print("[Warning] Attempted to remove event that was not subscribed.")
            return
        self._on_click_events.remove(event)

    def emit_on_click(self, trigger_event: Event):
        for e in self._on_click_events:
            e(self.position, trigger_event)
