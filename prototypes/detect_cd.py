import discid, threading, time

state = {"disc": None}  # latest result, read this from your frame loop

def _watch():
    prev_id = None
    while True:
        try:
            disc = discid.read()  # default drive; raises DiscError if empty/unreadable
        except discid.DiscError:
            disc = None
        cur_id = disc.id if disc else None
        if cur_id != prev_id:
            state["disc"] = disc
            prev_id = cur_id
        time.sleep(1)

threading.Thread(target=_watch, daemon=True).start()

# ---- your frame loop ----
shown = None
while True:
    disc = state["disc"]
    cur = disc.id if disc else None
    if cur != shown:
        shown = cur
        if disc:
            print(f"cd inserted: {len(disc.tracks)} tracks, {disc.seconds}s")
            for t in disc.tracks:
                print(f"  track {t.number}: {t.seconds}s")
        else:
            print("cd removed / no disc")
    time.sleep(1 / 60)