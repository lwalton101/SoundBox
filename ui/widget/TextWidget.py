from typing import override

from pyray import BLACK, Color, Rectangle, draw_rectangle_rec, draw_text_pro, load_font, load_font_ex

from events import Event
from ui.WindowState import WindowState
from ui.widget.Widget import Widget

class TextWidget(Widget):

    def __init__(self, state: WindowState, x: float, y: float) -> None:
        super().__init__(state, x, y)
        self.font_size = 56
        self.font = load_font_ex("assets/RobotoMono.ttf", self.font_size, None, 255)

    @override
    def draw(self, x: float, y: float):
        draw_text_pro(self.font, "test text", (x, y), (0,0), 0, self.font_size, -3, BLACK)
