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

    def draw(self, x: float, y: float):
        pass

    def render(self, parentX: float, parentY: float):
        if not self.visible:
            return

        absolute_x = parentX + self.x
        absolute_y = parentY + self.y

        self.draw(absolute_x, absolute_y)

        for child in self.children:
            child.render(absolute_x, absolute_y)
