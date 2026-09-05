from typing import override

from pyray import Color, Rectangle, draw_rectangle_rec

from ui.WindowState import WindowState
from ui.widget.Widget import Widget

class RectWidget(Widget):
    width: float
    height: float
    color: Color

    def __init__(self, state: WindowState, x: float, y: float, width: int, height: int, color: Color) -> None:
        super().__init__(state, x, y)
        self.width = width
        self.height = height
        self.color = color

    @override
    def render(self, parentX: float, parentY: float):
        x = self.x + parentX
        y = self.y + parentY

        draw_rectangle_rec(
            Rectangle(x, y, self.width, self.height),
            self.color,
        )
        super().render(x, y)
