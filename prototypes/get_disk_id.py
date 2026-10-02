import discid

def get_disc_id():
    try:
        disc = discid.read()
        return disc
    except discid.DiscError as e:
        print(f"Can't read disc: {e}")

print(get_disc_id())
