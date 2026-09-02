from pyray import VIOLET,WHITE, begin_drawing, clear_background, close_window, draw_fps, draw_text, end_drawing, init_window, set_target_fps, window_should_close

from ui.WindowState import WindowState


class Window:
    state: WindowState
    def __init__(self):
        self.state = WindowState()
        init_window(1280, 800, self.state.window_title)
        set_target_fps(self.state.fps_cap)
        pass


    def render(self) -> bool:
        begin_drawing()
        clear_background(WHITE)  # noqa: F821
        draw_text("Hello world", 190, 200, 20, VIOLET)
        draw_fps(10,10)
        end_drawing()
        return window_should_close()

    def close(self):
        close_window()
