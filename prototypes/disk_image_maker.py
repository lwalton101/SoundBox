from PIL import Image

def is_in_circle(circle_x: int, circle_y: int, radius: int, pos_x: int, pos_y: int) -> bool:
    return (pos_x - circle_x) ** 2 + (pos_y - circle_y) ** 2 < radius ** 2

image = Image.open("./assets/hamilton.jpg").convert("RGBA")
image = image.resize((500, 500))
image_middle = (image.size[0] / 2, image.size[1] / 2)

small_radius = 25

large_radius = 200

for x in range(image.size[0]):
    for y in range(image.size[1]):
        if is_in_circle(int(image_middle[0]), int(image_middle[1]), small_radius, x, y):
            image.putpixel((x,y), (255,255,255,0))

        if not is_in_circle(int(image_middle[0]), int(image_middle[1]), large_radius, x, y):
            image.putpixel((x,y), (255,255,255,0))
image.show()
