from typing import List, Self, final

from pyray import get_frame_time

from events import Event
from ui.WindowState import WindowState


class Widget():
    children: list["Widget"]
    x: float
    y: float
    visible: bool
    active: bool
    def __init__(self, state: WindowState, x: float, y: float) -> None:
        self.state = state
        self.children = []
        self.x = x
        self.y = y
        self.visible = True
        self.active = True
        pass

    def draw(self, x: float, y: float):
        pass

    def render(self, parentX: float, parentY: float):
        if not self.visible:
            return

        absolute_x = parentX + self.x
        absolute_y = parentY + self.y

        self.draw(absolute_x, absolute_y)

        for child in self.children:
            child.render(absolute_x, absolute_y)

    def on_update(self, dt: float):
        pass

    @final
    def update(self, dt: float):
        if not self.active:
            return

        self.on_update(dt)

        for child in self.children:
            child.update(dt)

    def on_event(self, event: Event):
        pass

    @final
    def trigger_event(self, event: Event):
        if not self.active:
            return

        self.on_event(event)

        for child in self.children:
            child.on_event(event)
