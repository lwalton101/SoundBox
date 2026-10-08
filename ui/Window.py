import os

from pyray import BLUE, GRAY, RED, VIOLET,WHITE, begin_drawing, Color, clear_background, close_window, draw_fps, draw_text, end_drawing, get_frame_time, init_window, is_key_pressed, poll_input_events, set_config_flags, set_target_fps, set_window_title, window_should_close
from raylib import FLAG_MSAA_4X_HINT, FLAG_VSYNC_HINT, FLAG_WINDOW_UNDECORATED
from os import listdir
from os.path import isfile, join
from events import Event
from ui.WindowState import WindowState
from ui.widget.ChangingImageWidget import ChangingImageWidget
from ui.widget.CircleWidget import CircleWidget
from ui.widget.ImageWidget import ImageWidget
from ui.widget.LineWidget import LineWidget
from ui.widget.ListWidget import ListWidget
from ui.widget.EventDebugWidget import EventDebugWidget
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
        
        self.album_image = ChangingImageWidget(self.state, 1280 / 100 * 35, 300, 500, 500, "discs/5817355c-0ea6-4662-877f-3070c262b124.png", file_paths= [f"discs/{f}" for f in listdir("./assets/discs") if isfile(join("./assets/discs", f))], centered=True)
        self.root_widget.children.append(self.album_image)
        
        self.song_title = TextWidget(self.state, 1280 / 100 * 35, 600, font_size=TextWidget.LARGE_SIZE, centered=True, text="the cure")
        self.root_widget.children.append(self.song_title)
        
        self.artist = TextWidget(self.state, 1280 / 100 * 35, 640, font_size=TextWidget.MEDIUM_SIZE, centered=True, text="Olivia Rodrigo", color=GRAY, spacing=-1)
        self.root_widget.children.append(self.artist)
        
        self.bar = RectWidget(self.state, 1280 / 100 * 35- 200, 690, width=400, height=8, roundness=10, segments=100, color=GRAY)
        self.root_widget.children.append(self.bar)
        
        self.progress_circle = CircleWidget(self.state, 1280 / 100 * 35- 200 + (4 * 25), 690 + 8 / 2, 16, BLUE)
        self.root_widget.children.append(self.progress_circle)
        
        self.test_circle = PolyWidget(self.state, 100, 100, 750, 50, 0, RED)
        self.root_widget.children.append(self.test_circle)
        
        self.progress_text = TextWidget(self.state, 1280 / 100 * 35, 735, TextWidget.MEDIUM_SIZE, text="1:14 / 4:57", centered=True, color=GRAY)
        self.root_widget.children.append(self.progress_text)
        
        self.dividing_line = LineWidget(self.state, 1280 / 100 * 70, 0, horizontal=False, length=1280, thickness=3, color=GRAY)
        self.root_widget.children.append(self.dividing_line)
        
        self.album_title = TextWidget(self.state, 1280 / 100 * 85, 38, TextWidget.LARGE_SIZE, text="Unreal Unearth", centered=True, spacing=-1)
        self.root_widget.children.append(self.album_title)
        
        self.dividing_line_album = LineWidget(self.state, 1280 / 100 * 70, 80, horizontal=True, length=1280 / 100 * 30, thickness=3, color=GRAY)
        self.root_widget.children.append(self.dividing_line_album)
        i = 0
        for x in ["1 - all-american bitch", "2 - bad idea right?", "3 - vampire", "4 - lacy", "5 - ballad of a homesch..."]:
            color = GRAY
            if i == 2:
                color = WHITE
            text = TextWidget(self.state, 1280 / 100 * 70 + 10, 90 + i * 60, font_size=TextWidget.MEDIUM_SIZE, text=x, color=color, spacing=0)
            self.root_widget.children.append(text)
            i += 1
            
            
        self.event_debug = EventDebugWidget(self.state, 0,0)
        self.root_widget.children.append(self.event_debug)
        
        self.time = 0

    def on_title_changed(self, title: str):
        set_window_title(title)

    def on_fps_cap_changed(self, fps_cap: int):
        set_target_fps(fps_cap)

    def render(self) -> bool:
        begin_drawing()
        clear_background(self.state.background_color.get())  # noqa: F821

        self.root_widget.render(0,0)
        draw_fps(10,10)
        end_drawing()
        return window_should_close()

    def update(self):
        self.root_widget.update(get_frame_time())
        
        self.time += get_frame_time()
        if self.time > 1:
            self.progress_circle.x += 1
            self.time = 0

    def trigger_event(self, event: Event):
        self.root_widget.trigger_event(event)

    def close(self):
        close_window()
