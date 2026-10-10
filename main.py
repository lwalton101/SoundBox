from api.server.WebsocketServer import WebsocketServer
from events import Event
from ui.Window import Window
from music.audio_player import AudioPlayer
from ui.fonts import Fonts
from ui.textures import Textures
import musicbrainzngs

print("Soundbox initialising")

musicbrainzngs.set_useragent("SoundBox", "beta", "luke.walton@outlook.com")

window = Window()
should_close = False

api_server = WebsocketServer()
api_server.start()


while not should_close:
    events = []
    #get events from api server
    while not api_server.events.empty():
        events.append(api_server.events.get())
        
    while not window.state.audio_player.get().events_to_process.empty():
        events.append(window.state.audio_player.get().events_to_process.get())

    for event in events:
        window.trigger_event(event)
    window.update()
    should_close = window.render()
    Fonts.clear_cached_fonts()
    Textures.clear_cached_images()

window.close()
api_server.stop()
