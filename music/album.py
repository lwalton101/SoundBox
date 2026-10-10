from music.track import Track


class Album:
    def __init__(self, name: str, disc_id: str, release_id: str | None, tracks: list[Track]) -> None:
        self.name = name
        self.disc_id = disc_id
        self.release_id = release_id
        self.tracks = tracks