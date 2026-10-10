from typing import override

from pyray import Color, Rectangle, draw_rectangle_rec, draw_rectangle_rounded

from events import Event
from ui.WindowState import WindowState
from ui.widget.Widget import Widget

class ScreenWidget(Widget):
    width: float
    height: float
    color: Color

    def __init__(self, state: WindowState, x: float, y: float, width: float, height: float) -> None:
        super().__init__(state, x, y)
        self.width = width
        self.height = height
