import random
from typing import override

from events import Event
from ui.WindowState import WindowState
from ui.widget.ImageWidget import ImageWidget


class ChangingImageWidget(ImageWidget):
    def __init__(self, state: WindowState, x: float, y: float, width: float, height: float, file_path: str = "", file_paths: list[str] = [], centered: bool = False) -> None:
        super().__init__(state, x, y, width, height, file_path, centered)
        self.file_paths = file_paths
        
    @override
    def on_event(self, event: Event):
        if event == Event.VOLUME_UP:
            print("change image")
            self.load_image(random.choice(self.file_paths))