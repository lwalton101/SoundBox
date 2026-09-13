from api.server.WebsocketServer import WebsocketServer
from events import Event
from ui.Window import Window

print("Soundbox initialising")

window = Window()
should_close = False

api_server = WebsocketServer()
api_server.start()

while not should_close:
    events = []
    #get events from api server
    while not api_server.events.empty():
        events.append(api_server.events.get())

    for event in events:
        window.trigger_event(event)
    window.update()
    should_close = window.render()

window.close()
api_server.stop()
