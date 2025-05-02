from dataclasses import dataclass
from tkinter import Canvas, Event
from MathLib.Vector import Vector2I
from typing import Callable, List, Optional
from Worker import Worker


@dataclass
class TileState:
    def __init__(self, position: Vector2I):
        self.position = position
        self.stack_height: int = 0
        self.worker: Optional[Worker] = None
        self.on_click_events: List[Callable[[
            "Event[Canvas]", Vector2I], None]] = []

    def connect_on_click(self, event: Callable[["Event[Canvas]", Vector2I], None]):
        if event in self.on_click_events:
            print("[Warning] Event already connected.")
            return
        self.on_click_events.append(event)

    def disconnect_on_click(self, event: Callable[["Event[Canvas]", Vector2I], None]):
        if not event in self.on_click_events:
            print("[Warning] Attempted to remove event that was not connected.")
            return
        self.on_click_events.remove(event)

    def emit_on_click(self, trigger: "Event[Canvas]"):
        print(f"[Notice] Tile @ {self.position} clicked, emitting signal.")
        for e in self.on_click_events:
            e(trigger, self.position)
