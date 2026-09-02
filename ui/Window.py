from pyray import VIOLET,WHITE, begin_drawing, clear_background, close_window, draw_fps, draw_text, end_drawing, init_window, is_key_pressed, poll_input_events, set_target_fps, set_window_title, window_should_close
from raylib.defines import KEY_LEFT

from ui.WindowState import WindowState


class Window:
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
        draw_text("Hello world", 190, 200, 20, VIOLET)
        draw_fps(10,10)
        end_drawing()
        return window_should_close()

    def close(self):
        close_window()
