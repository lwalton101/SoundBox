from typing import override

from pyray import Color, Vector2, draw_poly

from ui.WindowState import WindowState
from ui.widget.Widget import Widget


class PolyWidget(Widget):
    sides: int
    radius: float
    rotation: float
    color: Color

    def __init__(self, state: WindowState, x: float, y: float, sides: int, radius: float, rotation: float, color: Color) -> None:
        super().__init__(state, x, y)
        self.color = color
        self.sides = sides
        self.radius = radius
        self.rotation = rotation

    @override
    def draw(self, x: float, y: float):
        draw_poly(Vector2(self.x, self.y), self.sides, self.radius, self.rotation, self.color)
