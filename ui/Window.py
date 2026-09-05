from pyray import VIOLET,WHITE, begin_drawing, Color, clear_background, close_window, draw_fps, draw_text, end_drawing, get_frame_time, init_window, is_key_pressed, poll_input_events, set_target_fps, set_window_title, window_should_close

from ui.WindowState import WindowState
from ui.widget.PolyWidget import PolyWidget
from ui.widget.RectWidget import RectWidget
from ui.widget.Widget import Widget

class Window:
    startX: float = 0
    startY: float = 0
    state: WindowState
    def __init__(self):
        self.state = WindowState()
        init_window(1280, 800, self.state.window_title.get())
        set_target_fps(self.state.fps_cap.get())

        self.state.window_title.subscribe(self.on_title_changed)
        self.state.fps_cap.subscribe(self.on_fps_cap_changed)
        pass

    def on_title_changed(self, title: str):
        set_window_title(title)

    def on_fps_cap_changed(self, fps_cap: int):
        set_target_fps(fps_cap)

    def render(self) -> bool:
        begin_drawing()
        clear_background(WHITE)  # noqa: F821
        root_widget = Widget(self.state, 0,0)
        rect_widget = RectWidget(self.state, self.startX, self.startY, 500, 30, Color(255,0,0,255))
        rect_widget_two = RectWidget(self.state, 0, 50, 500, 30, Color(0,0,255,255))
        rect_widget_three = RectWidget(self.state, 0, 50, 500, 30, Color(0,255,0,255))

        triangle = PolyWidget(self.state, 500, 600, 6, 150, 0, Color(0, 255, 0, 255))
        root_widget.children.append(rect_widget)
        root_widget.children.append(triangle)
        rect_widget.children.append(rect_widget_two)
        rect_widget_two.children.append(rect_widget_three)

        self.startX += 10 * get_frame_time()

        if self.startX > 1280:
            self.startX = 0

        root_widget.render(0,0)
        draw_fps(10,10)
        end_drawing()
        return window_should_close()

    def close(self):
        close_window()
