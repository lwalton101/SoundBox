from typing import override

from pyray import BLACK, Color, Rectangle, draw_rectangle_rec, draw_text_pro, load_font, load_font_ex

from events import Event
from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget

class TextWidget(Widget):
    def __init__(self, state: WindowState, x: float, y: float) -> None:
        super().__init__(state, x, y)
        self.font_size = 100
        self.ticker: float = 0
    @override
    def draw(self, x: float, y: float):
        font = Fonts.get_font("RobotoMono", self.font_size)
        draw_text_pro(font, "test text", (x, y), (0,0), 0, self.font_size, -3, BLACK)

    @override
    def on_update(self, dt: float):
        self.ticker += 1 * dt
        if self.ticker > 0.1:
            self.ticker = 0
            self.font_size += 1
