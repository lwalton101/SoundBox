from typing import Self

from ui.WindowState import WindowState


class Widget():
    children: list[Self]
    x: int
    y: int
    def __init__(self, state: WindowState, x: int, y: int) -> None:
        self.state = state
        self.children = []
        self.x = x
        self.y = y
        pass

    def render(self, parentX: int, parentY: int):
        for child in self.children:
            child.render(self.x, self.y)
        pass
