from typing import override

from pyray import GRAY, WHITE

from events import Event
from ui.WindowState import WindowState
from ui.widget.ImageWidget import ImageWidget
from ui.widget.TextWidget import TextWidget
from ui.widget.screen.ScreenWidget import ScreenWidget


class AlbumScreenWidget(ScreenWidget):
    def __init__(self, state: WindowState, x: float, y: float, width: float, height: float) -> None:
        super().__init__(state, x, y, width, height)
        
        self.album_image_height = 38
        self.song_title_height = 75
        
        self.album_image = ImageWidget(self.state, width // 2, height / 100 * self.album_image_height, 500, 500, "discs/5817355c-0ea6-4662-877f-3070c262b124.png", centered=True)
        self.children.append(self.album_image)
        
        self.song_title = TextWidget(self.state, width // 2, height / 100 * self.song_title_height, font_size=TextWidget.LARGE_SIZE, centered=True, text="the cure", max_width=width)
        self.children.append(self.song_title)
        
    @override
    def on_event(self, event: Event):
        if event == Event.DISC_ENTER or event == Event.DISC_EXIT:
            self.set_album()
            
    def set_album(self):
        
        album = self.state.audio_player.get().album()
        
        self.song_title.text = "No Song Playing"
        
        if album == None:
            self.song_title.text = "No Disc entered"
            self.album_image.load_image("no_disc.png")
            return
        
        self.album_image.load_image(f"discs/{album.disc_id}.png")
        pass
            