from typing import override

from pyray import Color, Rectangle, draw_circle, draw_rectangle_rec, draw_rectangle_rounded

from events import Event
from ui.WindowState import WindowState
from ui.widget.Widget import Widget

class CircleWidget(Widget):

    def __init__(self, state: WindowState, x: float, y: float, radius: float, color: Color) -> None:
        super().__init__(state, x, y)
        self.radius = radius
        self.color = color

    @override
    def draw(self, x: float, y: float):
        draw_circle(int(x), int(y), self.radius, self.color)
