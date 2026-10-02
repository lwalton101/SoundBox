from typing import override

from events import Event
from ui.WindowState import WindowState
from ui.widget.Widget import Widget


class EventDebugWidget(Widget):

    def __init__(self, state: WindowState, x: float, y: float) -> None:
        super().__init__(state, x, y)

    @override
    def on_event(self, event: Event):
        print(f"Event triggered: {event}")
