from io import BytesIO
import json
import os
from queue import Queue
import threading, time

import discid, musicbrainzngs
import requests

from events import Event
from music.album import Album
from music.track import Track
from PIL import Image, UnidentifiedImageError, ImageOps

musicbrainzngs.set_useragent("SoundBox", "beta", "luke.walton@outlook.com")
class AudioPlayer:
    def __init__(self):
        self.drive_watch_thread = threading.Thread(target=self._watch_drive, daemon=True)
        self.drive_watch_thread.start()
        
        self.events_to_process = Queue()
        self._album_lock = threading.Lock()
        self._album = None
        self.has_album_been_detected = False
        pass
    
    def album(self) -> Album | None:
        with self._album_lock:
            return self._album
        
    def set_album(self, album):
        with self._album_lock:
            if self._album == album and self.has_album_been_detected:
                return
            self._album = album
            self.has_album_been_detected = True
            if self.has_album_been_detected:
                print("we got past and album detected")
            if album == None:
                self.events_to_process.put(Event.DISC_EXIT)
            else:
                self.events_to_process.put(Event.DISC_ENTER)
    
    def _watch_drive(self):
        prev_id = None
        while True:
            try:
                disc = discid.read()  # default drive; raises DiscError if empty/unreadable
            except discid.DiscError as e:
                disc = None
                
            if disc == None:
                prev_id = None
                self.set_album(None)
                continue
            
            cur_id = disc.id
            if cur_id != prev_id:
                prev_id = disc.id
                print(disc.id)
                self.set_album(self.get_album_from_disc(disc))
                
            time.sleep(3)
            
    def get_image_from_release_id(self, release_id, disc_id):
        print("downloading image")
        if os.path.exists(f"assets/discs/{disc_id}.png"):
            print("Image already downloaded")
            return
        
        images = []
        try:
            images = musicbrainzngs.get_image_list(release_id)["images"]
        except Exception as e:
            print("error getting image from release id")
            print(e)
            
        front_detected = False
        for image in images:
            if image["front"]:
                front_detected = True
                
        for image in images:
            if not image["front"] and front_detected:
                continue
            
            print(image["image"])
            response = requests.get(image["image"])
            img = Image.open("./assets/no_disc.png")
            try: 
                img = Image.open(BytesIO(response.content))
            except UnidentifiedImageError:
                print(response.content)
            img = ImageOps.contain(img, (500, 500), Image.Resampling.LANCZOS)
            print(img.size)
            img.save(f"assets/discs/{disc_id}.png")
            continue
            
    def get_album_from_disc(self, disc: discid.Disc) -> Album:
        disc_id = disc.id
        try:
            releases = musicbrainzngs.get_releases_by_discid(disc_id)["disc"]["release-list"]
        except musicbrainzngs.ResponseError:
            tracks = [Track(None, track.number, track.number, track.seconds * 1000, "Unknown Artist", f"Track {track.number}") for track in disc.tracks]
            return Album("Unknown Album", disc_id, None, tracks)
        release_id = releases[0]["id"]
        
        release = musicbrainzngs.get_release_by_id(release_id, includes=["recordings", "artist-credits"])["release"]
        medium = release["medium-list"][0]
        
        tracks: list[Track] = []
        for track_dict in medium["track-list"]:
            title = track_dict["recording"]["title"]
            artist = track_dict["artist-credit-phrase"]
            print(f"' : {ord("'")}")
            for char in artist:
                print(f"{char}: {ord(char)}")
            tracks.append(Track(track_dict["id"], track_dict["position"], track_dict["number"], int(track_dict["length"]), track_dict["artist-credit-phrase"].replace("‐", "-"), title.replace("’", "'")))
            
        self.get_image_from_release_id(release_id, disc_id)
        return Album(release["title"], disc_id, release_id, tracks)
    
            