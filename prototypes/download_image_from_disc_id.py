from io import BytesIO
import requests

import musicbrainzngs
from PIL import Image, ImageOps, UnidentifiedImageError

DISC_ID = "AJJqJcnSJd1qhyRHKw7tue5rSWE-"

musicbrainzngs.set_useragent("Soundbox", "beta", "luke.walton@outlook.com")

def get_image_from_release_id(release_id):
    images = []
    try:
        images = musicbrainzngs.get_image_list(release_id)["images"]
    except Exception as e:
        print("error getting image from release id")
        print(e)
    for image in images:
        if not image["front"]:
            continue
        
        print(image["image"])
        response = requests.get(image["image"])
        img = Image.open("./assets/no_disc.png")
        try: 
            img = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            print(response.content)
        img = ImageOps.contain(img, (500, 500), Image.LANCZOS)
        print(img.size)
        img.save(f"assets/discs/{release_id}.png")
        continue
        
        
ids = [x.strip() for x in open("assets/release-ids.txt").readlines()]


get_image_from_release_id("8867a105-f711-41ca-9e36-d443554306e6")
for id in ids:
    print(id)    
    get_image_from_release_id(id)