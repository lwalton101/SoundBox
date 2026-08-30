from pyray import init_window, begin_drawing, clear_background, draw_text, end_drawing, window_should_close, WHITE, VIOLET, close_window
import os

os.environ["DISPLAY"] = ":0"

init_window(1280, 800, "SoundBox")
while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    draw_text("Hello world", 190, 200, 20, VIOLET)
    end_drawing()
close_window()
