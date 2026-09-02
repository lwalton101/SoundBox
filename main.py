from ui.Window import Window

print("Soundbox initialising")

window = Window()
should_close = False

while not should_close:
    should_close = window.render()

window.close()
