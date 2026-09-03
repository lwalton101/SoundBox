from typing import override

from pyray import Color, draw_rectangle

from ui.WindowState import WindowState
from ui.widget.Widget import Widget


class RectWidget(Widget):
    width: int
    height: int
    color: Color

    def __init__(self, state: WindowState, x: int, y: int, width: int, height: int, color: Color) -> None:
        super().__init__(state, x, y)
        self.width = width
        self.height = height
        self.color = color

    @override
    def render(self, parentX: int, parentY: int):
        draw_rectangle(self.x + parentX, self.y + parentY, self.width, self.height, self.color)
        super().render(self.x, self.y)
