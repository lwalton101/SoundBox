from typing import override

from pyray import Color, Vector2, draw_poly

from ui.WindowState import WindowState
from ui.widget.Widget import Widget


class PolyWidget(Widget):
    sides: int
    radius: float
    rotation: float
    color: Color

    def __init__(self, state: WindowState, x: int, y: int, sides: int, radius: float, rotation: float, color: Color) -> None:
        super().__init__(state, x, y)
        self.color = color
        self.sides = sides
        self.radius = radius
        self.rotation = rotation

    @override
    def render(self, parentX: int, parentY: int):
        draw_poly(Vector2(self.x + parentX, self.y + parentY), self.sides, self.radius, self.rotation, self.color)
        super().render(self.x, self.y)
