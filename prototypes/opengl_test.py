import glfw
from OpenGL.GL import *
from PIL import Image
import time


# --------------------------------------------------
# Settings
# --------------------------------------------------

WIDTH = 1280
HEIGHT = 800

SQUARE_SIZE = 450
ROTATION_SPEED = 30.0       # degrees per second

TEXTURE_PATH = "assets/hamilton.jpg"
TEXTURE_MAX_SIZE = 512

MSAA_SAMPLES = 4


# --------------------------------------------------
# Load texture
# --------------------------------------------------

def load_texture(path):
    image = Image.open(path).convert("RGB")

    # Reduce texture size for Raspberry Pi 3
    image.thumbnail(
        (TEXTURE_MAX_SIZE, TEXTURE_MAX_SIZE),
        Image.Resampling.LANCZOS
    )

    # Flip vertically for OpenGL
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    width, height = image.size
    pixels = image.tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # RGB rows are not always aligned to 4 bytes
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Smooth texture filtering
    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
    )

    # Prevent texture bleeding at the edges
    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_S,
        GL_CLAMP_TO_EDGE
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_T,
        GL_CLAMP_TO_EDGE
    )

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGB,
        width,
        height,
        0,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        pixels
    )

    glBindTexture(GL_TEXTURE_2D, 0)

    print(f"Texture size: {width}x{height}")

    return texture


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # --------------------------------------------------
    # GLFW
    # --------------------------------------------------

    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # OpenGL 2.1
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    # 4x Multisample Anti-Aliasing
    glfw.window_hint(glfw.SAMPLES, MSAA_SAMPLES)

    window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "OpenGL Textured Square",
        None,
        None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)

    # Disable VSync for performance testing
    glfw.swap_interval(0)

    # --------------------------------------------------
    # OpenGL information
    # --------------------------------------------------

    print(
        "OpenGL version:",
        glGetString(GL_VERSION).decode()
    )

    print(
        "OpenGL renderer:",
        glGetString(GL_RENDERER).decode()
    )

    print(
        "OpenGL vendor:",
        glGetString(GL_VENDOR).decode()
    )

    # Check MSAA
    samples = glGetIntegerv(GL_SAMPLES)

    print("MSAA samples:", samples)

    # --------------------------------------------------
    # OpenGL state
    # --------------------------------------------------

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)

    glEnable(GL_TEXTURE_2D)

    # Enable multisample anti-aliasing
    glEnable(GL_MULTISAMPLE)

    # --------------------------------------------------
    # Framebuffer size
    # --------------------------------------------------

    framebuffer_width, framebuffer_height = (
        glfw.get_framebuffer_size(window)
    )

    glViewport(
        0,
        0,
        framebuffer_width,
        framebuffer_height
    )

    # --------------------------------------------------
    # Projection
    # --------------------------------------------------

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(
        0,
        framebuffer_width,
        framebuffer_height,
        0,
        -1,
        1
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --------------------------------------------------
    # Load texture
    # --------------------------------------------------

    texture = load_texture(TEXTURE_PATH)

    # --------------------------------------------------
    # Timing
    # --------------------------------------------------

    rotation = 0.0

    previous_time = time.perf_counter()

    fps_timer = previous_time
    frame_count = 0

    # --------------------------------------------------
    # Main loop
    # --------------------------------------------------

    while not glfw.window_should_close(window):

        current_time = time.perf_counter()

        dt = current_time - previous_time
        previous_time = current_time

        # Prevent a huge rotation jump after a pause
        dt = min(dt, 0.1)

        # Constant rotation speed
        rotation += ROTATION_SPEED * dt

        if rotation >= 360.0:
            rotation -= 360.0

        # --------------------------------------------------
        # Clear
        # --------------------------------------------------

        glClearColor(
            0.0,
            0.0,
            0.0,
            1.0
        )

        glClear(GL_COLOR_BUFFER_BIT)

        # --------------------------------------------------
        # Model matrix
        # --------------------------------------------------

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Move to screen center
        glTranslatef(
            framebuffer_width / 2.0,
            framebuffer_height / 2.0,
            0.0
        )

        # Rotate around the center
        glRotatef(
            rotation,
            0.0,
            0.0,
            1.0
        )

        # Move quad so its center is at (0, 0)
        half_size = SQUARE_SIZE / 2.0

        glTranslatef(
            -half_size,
            -half_size,
            0.0
        )

        # --------------------------------------------------
        # Bind texture
        # --------------------------------------------------

        glBindTexture(
            GL_TEXTURE_2D,
            texture
        )

        # --------------------------------------------------
        # Draw textured quad
        # --------------------------------------------------

        glBegin(GL_QUADS)

        # Top-left
        glTexCoord2f(0.0, 0.0)
        glVertex2f(
            0.0,
            0.0
        )

        # Top-right
        glTexCoord2f(1.0, 0.0)
        glVertex2f(
            SQUARE_SIZE,
            0.0
        )

        # Bottom-right
        glTexCoord2f(1.0, 1.0)
        glVertex2f(
            SQUARE_SIZE,
            SQUARE_SIZE
        )

        # Bottom-left
        glTexCoord2f(0.0, 1.0)
        glVertex2f(
            0.0,
            SQUARE_SIZE
        )

        glEnd()

        glBindTexture(
            GL_TEXTURE_2D,
            0
        )

        # --------------------------------------------------
        # Display
        # --------------------------------------------------

        glfw.swap_buffers(window)
        glfw.poll_events()

        # --------------------------------------------------
        # FPS
        # --------------------------------------------------

        frame_count += 1

        if current_time - fps_timer >= 1.0:

            fps = (
                frame_count /
                (current_time - fps_timer)
            )

            print(f"FPS: {fps:.1f}")

            frame_count = 0
            fps_timer = current_time

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    glDeleteTextures([texture])

    glfw.destroy_window(window)
    glfw.terminate()


# --------------------------------------------------
# Start
# --------------------------------------------------

if __name__ == "__main__":
    main()
