from typing import override

from pyray import BLACK, WHITE, Color, draw_line, draw_line_ex, draw_text_pro

from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget

class LineWidget(Widget):
    
    def __init__(self, state: WindowState, x: float, y: float, color: Color = WHITE, length: float = 100.0, thickness: float = 1.0) -> None:
        super().__init__(state, x, y)
        self.color = color
        self.length = length
        self.thickness = thickness
        
    @override
    def draw(self, x: float, y: float):
        draw_line_ex((x, y), (x + self.length, y), self.thickness, self.color)
