from typing import override

from pyray import BLACK, Color, Rectangle, draw_rectangle_rec, draw_text_pro, load_font, load_font_ex

from events import Event
from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget

class TextWidget(Widget):
    LARGE_SIZE: int = 64
    MEDIUM_SIZE: int = 32
    SMALL_SIZE: int = 16
    def __init__(self, state: WindowState, x: float, y: float, font_size: int = LARGE_SIZE, spacing: int = -2) -> None:
        super().__init__(state, x, y)
        self.font_size = font_size
        self.spacing = spacing
    @override
    def draw(self, x: float, y: float):
        font = Fonts.get_font("RobotoMono", self.font_size)
        draw_text_pro(font, "test text", (x, y), (0,0), 0, self.font_size, self.spacing, BLACK)
