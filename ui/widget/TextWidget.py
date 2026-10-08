from typing import override

from pyray import BLACK, WHITE, Color, Vector2, draw_text_pro, measure_text_ex

from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget

class TextWidget(Widget):
    LARGE_SIZE: int = 50
    MEDIUM_SIZE: int = 32
    SMALL_SIZE: int = 16
    def __init__(self, state: WindowState, x: float, y: float, font_size: int = LARGE_SIZE, spacing: int = -2, text: str = "test text", color: Color = WHITE, centered: bool = False) -> None:
        super().__init__(state, x, y)
        self.font_size = font_size
        self.spacing = spacing
        self.text = text
        self.color = color
        self.centered = centered
        self.font = Fonts.get_font("RobotoMono", self.font_size)
        
    @override
    def draw(self, x: float, y: float):
        self.font = Fonts.get_font("RobotoMono", self.font_size)
        pos = (x, y)
        
        if self.centered:
            pos = (pos[0] - self.get_text_dim().x / 2, pos[1] - self.get_text_dim().y / 2)
        draw_text_pro(self.font, self.text, pos, (0,0), 0, self.font_size, self.spacing, self.color)
        
    def get_text_dim(self) -> Vector2:
        return measure_text_ex(self.font, self.text, self.font_size, self.spacing)
        
        
