from typing import override

from ui.WindowState import WindowState
from ui.widget.LineWidget import LineWidget
from ui.widget.TextWidget import TextWidget
from ui.widget.Widget import Widget

class ListWidget(Widget):
    def __init__(self, state: WindowState, x: float, y: float, spacing: int = 15, items: list[str] = [], text_size: int = TextWidget.LARGE_SIZE, line_length = 100) -> None:
        super().__init__(state, x, y)
        self.spacing = spacing
        self.items = items
        self.text_size = text_size
        self.line_length = 100

        i = 0
        for item in items:
            i += 1
            text_widget = TextWidget(state, 0, i * self.spacing, font_size=self.text_size, text=item, centered=True)
            text_dims = text_widget.get_text_dim()
            self.children.append(text_widget)
            
            self.children.append(LineWidget(state, x - text_dims.x / 2, i * spacing, thickness=2))

    @override
    def draw(self, x: float, y: float):
        
        pass
