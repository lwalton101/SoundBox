from typing import Self

from ui.WindowState import WindowState


class Widget():
    children: list["Widget"]
    x: float
    y: float
    visible: bool
    def __init__(self, state: WindowState, x: float, y: float) -> None:
        self.state = state
        self.children = []
        self.x = x
        self.y = y
        self.visible = True
        pass

    def render(self, parentX: float, parentY: float):
        if not self.visible:
            return

        for child in self.children:
            child.render(parentX, parentY)
