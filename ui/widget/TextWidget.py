from typing import override

from pyray import BLACK, WHITE, Color, draw_text_pro

from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget

class TextWidget(Widget):
    LARGE_SIZE: int = 50
    MEDIUM_SIZE: int = 32
    SMALL_SIZE: int = 16
    def __init__(self, state: WindowState, x: float, y: float, font_size: int = LARGE_SIZE, spacing: int = -2, text: str = "test text", color: Color = WHITE) -> None:
        super().__init__(state, x, y)
        self.font_size = font_size
        self.spacing = spacing
        self.text = text
        self.color = color
        
    @override
    def draw(self, x: float, y: float):
        font = Fonts.get_font("Aldrich-Regular", self.font_size)
        draw_text_pro(font, self.text, (x, y), (0,0), 0, self.font_size, self.spacing, self.color)
