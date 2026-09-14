import os

from pyray import VIOLET,WHITE, begin_drawing, Color, clear_background, close_window, draw_fps, draw_text, end_drawing, get_frame_time, init_window, is_key_pressed, poll_input_events, set_config_flags, set_target_fps, set_window_title, window_should_close
from raylib import FLAG_MSAA_4X_HINT, FLAG_VSYNC_HINT, FLAG_WINDOW_UNDECORATED

from events import Event
from ui.WindowState import WindowState
from ui.widget.PolyWidget import PolyWidget
from ui.widget.RectWidget import RectWidget
from ui.widget.TextWidget import TextWidget
from ui.widget.Widget import Widget

class Window:
    state: WindowState
    def __init__(self):
        os.environ["DISPLAY"] = ":0"
        self.state = WindowState()
        set_config_flags(FLAG_VSYNC_HINT | FLAG_WINDOW_UNDECORATED)
        init_window(1280, 800, self.state.window_title.get())
        #set_target_fps(self.state.fps_cap.get())

        self.state.window_title.subscribe(self.on_title_changed)
        self.state.fps_cap.subscribe(self.on_fps_cap_changed)

        self.root_widget = Widget(self.state, 0,0)
        self.rect_widget = RectWidget(self.state, 0, 0, 500, 30, Color(255,0,0,255))
        self.rect_widget_two = RectWidget(self.state, 0, 50, 500, 30, Color(0,0,255,255))
        self.rect_widget_three = RectWidget(self.state, 0, 50, 500, 30, Color(0,255,0,255))

        self.triangle = PolyWidget(self.state, 500, 600, 15, 150, 45.5, Color(0, 255, 0, 255))
        self.root_widget.children.append(self.rect_widget)
        self.root_widget.children.append(self.triangle)
        self.rect_widget.children.append(self.rect_widget_two)
        self.rect_widget_two.children.append(self.rect_widget_three)

        self.rotating_rect = PolyWidget(self.state, 500, 500, 4, 150, 150, VIOLET)
        self.root_widget.children.append(self.rotating_rect)

        self.text_widget = TextWidget(self.state, 20, 400, font_size=TextWidget.LARGE_SIZE)
        self.root_widget.children.append(self.text_widget)
        pass

    def on_title_changed(self, title: str):
        set_window_title(title)

    def on_fps_cap_changed(self, fps_cap: int):
        set_target_fps(fps_cap)

    def render(self) -> bool:
        begin_drawing()
        clear_background(WHITE)  # noqa: F821

        self.root_widget.render(0,0)
        draw_fps(10,10)
        end_drawing()
        return window_should_close()

    def update(self):
        self.root_widget.update(get_frame_time())

    def trigger_event(self, event: Event):
        self.root_widget.trigger_event(event)

    def close(self):
        close_window()
