from events import Event
from ui.Window import Window

print("Soundbox initialising")

window = Window()
should_close = False

while not should_close:
    events = []
    #Gather events

    for event in events:
        window.trigger_event(event)
    window.update()
    should_close = window.render()

window.close()
