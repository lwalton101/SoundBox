from typing import override

from pyray import GRAY, WHITE

from events import Event
from ui.WindowState import WindowState
from ui.widget.TextWidget import TextWidget
from ui.widget.screen.ScreenWidget import ScreenWidget


class AlbumSelectWidget(ScreenWidget):
    def __init__(self, state: WindowState, x: float, y: float, width: float, height: float) -> None:
        super().__init__(state, x, y, width, height)
        
        self.album_title = TextWidget(self.state, width // 2, 38, TextWidget.LARGE_SIZE, text="No Album", centered=True, spacing=-1)
        self.children.append(self.album_title)
        
        self.track_texts: list[TextWidget] = []
        
        self.track_initial_height = 80
        self.track_spacing = 60
        self.track_detail_offset = 30
        
    @override
    def on_event(self, event: Event):
        if event == Event.DISC_ENTER or event == Event.DISC_EXIT:
            self.set_album()
            
    def set_album(self):
        #self.album_image.load_image(self.)
        album = self.state.audio_player.get().album()
        
        if album == None:
            self.album_title.text = "No Album"
            for track_text in self.track_texts:
                self.children.remove(track_text)
                
            self.track_texts.clear()
            return
        
        
        for track_text in self.track_texts:
            self.children.remove(track_text)
            
        self.track_texts.clear()
        
        self.album_title.text = album.name
        
        i = 0
        for track in album.tracks:
            color = GRAY
            if i == 2:
                color = WHITE
            track_text = TextWidget(self.state, 5, self.track_initial_height + i * self.track_spacing, font_size=TextWidget.MEDIUM_SIZE, text=f"{track.position} - {track.title}", color=color, spacing=0)
            track_detail_text = TextWidget(self.state, 5, self.track_initial_height + self.track_detail_offset + i * self.track_spacing, font_size=TextWidget.SMALL_SIZE, text=f"{track.artist_credit} - {track.get_formatted_length()}", color=GRAY, spacing=0)
            self.track_texts.append(track_text)
            self.track_texts.append(track_detail_text)
            self.children.append(track_detail_text)
            self.children.append(track_text)
            i += 1

        pass