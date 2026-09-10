import pyray as rl


def main():
    screen_width = 1280
    screen_height = 800

    rl.init_window(
        screen_width,
        screen_height,
        "raylib - rotating textured square"
    )

    rl.set_target_fps(60)

    # Load texture
    texture = rl.load_texture("assets/hamilton.jpg")

    # Square
    size = 450

    rect = rl.Rectangle(
        screen_width / 2 - size / 2,
        screen_height / 2 - size / 2,
        size,
        size
    )

    rotation = 0.0

    while not rl.window_should_close():

        # Rotate
        rotation += 30.0 * rl.get_frame_time()

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Source rectangle for the texture
        source = rl.Rectangle(
            0,
            0,
            texture.width,
            texture.height
        )

        # Draw the texture inside the square
        rl.draw_texture_pro(
            texture,
            source,
            rect,
            rl.Vector2(size / 2, size / 2),
            rotation,
            rl.WHITE
        )

        rl.draw_text(
            "Rotating Textured Square",
            10,
            10,
            30,
            rl.BLACK
        )

        rl.draw_fps(10, 50)

        rl.end_drawing()

    # Clean up
    rl.unload_texture(texture)
    rl.close_window()


if __name__ == "__main__":
    main()
