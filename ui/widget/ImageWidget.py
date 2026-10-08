from typing import override

from pyray import WHITE, Color, Rectangle, draw_rectangle_rec, draw_texture

from events import Event
from ui.WindowState import WindowState
from ui.textures import Textures
from ui.widget.Widget import Widget

class ImageWidget(Widget):
    def __init__(self, state: WindowState, x: float, y: float, width: float, height: float, file_path: str = "", centered: bool = False) -> None:
        super().__init__(state, x, y)
        self.width = width
        self.height = height
        self.load_image(file_path)
        self.centered = centered
        
    def load_image(self, file_path: str = ""):
        self.file_path = file_path
        self.texture = Textures.get_texture(file_path)

    @override
    def draw(self, x: float, y: float):
        self.texture = Textures.get_texture(self.file_path)
        xPos = x
        yPos = y
        if self.centered:
            xPos = x - self.texture.width / 2
            yPos = y - self.texture.height / 2
        draw_texture(self.texture, int(xPos), int(yPos), WHITE)
