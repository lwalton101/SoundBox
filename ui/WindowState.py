from pyray import BLACK, Color

from util.TrackedVar import TrackedVar


class WindowState:
    window_title: TrackedVar[str] = TrackedVar("Sound Box")
    fps_cap: TrackedVar[int] = TrackedVar(0)
    background_color: TrackedVar[Color] = TrackedVar(BLACK)
