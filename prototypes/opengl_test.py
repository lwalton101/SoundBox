import glfw
from OpenGL.GL import *
from PIL import Image
import time


WIDTH = 1280
HEIGHT = 800
SQUARE_SIZE = 450
TEXTURE_PATH = "assets/hamilton.jpg"


def load_texture(path):
    image = Image.open(path).convert("RGBA")

    # OpenGL texture origin is bottom-left.
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    width, height = image.size
    pixels = image.tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Important for RGBA textures.
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Mipmap filtering greatly reduces shimmering when rotated.
    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR_MIPMAP_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
    )

    # Don't repeat at the edges.
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

    # Upload base texture.
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        pixels
    )

    # Generate mipmaps.
    glGenerateMipmap(GL_TEXTURE_2D)

    # Optional anisotropic filtering.
    try:
        extensions = glGetString(GL_EXTENSIONS).decode()

        if "GL_EXT_texture_filter_anisotropic" in extensions:
            max_aniso = glGetFloatv(
                GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT
            )

            # Don't go crazy on a Pi 3.
            aniso = min(float(max_aniso), 4.0)

            glTexParameterf(
                GL_TEXTURE_2D,
                GL_TEXTURE_MAX_ANISOTROPY_EXT,
                aniso
            )

            print("Anisotropic filtering:", aniso)

    except Exception:
        pass

    glBindTexture(GL_TEXTURE_2D, 0)

    return texture


def main():

    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # OpenGL 2.1.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    # Request multisampling for smoother quad edges.
    glfw.window_hint(glfw.SAMPLES, 4)

    window = glfw.create_window(
        WIDTH,
        HEIGHT,
        "OpenGL Rotating Image",
        None,
        None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)

    # VSync.
    glfw.swap_interval(1)

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

    # ------------------------------------------------
    # OpenGL setup
    # ------------------------------------------------

    glEnable(GL_TEXTURE_2D)

    # Smooth polygon edges.
    glEnable(GL_MULTISAMPLE)

    # Use smooth shading.
    glShadeModel(GL_SMOOTH)

    # White texture colour.
    glColor4f(
        1.0,
        1.0,
        1.0,
        1.0
    )

    # ------------------------------------------------
    # Projection
    # ------------------------------------------------

    framebuffer_width, framebuffer_height = \
        glfw.get_framebuffer_size(window)

    glViewport(
        0,
        0,
        framebuffer_width,
        framebuffer_height
    )

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

    # ------------------------------------------------
    # Texture
    # ------------------------------------------------

    texture = load_texture(TEXTURE_PATH)

    # ------------------------------------------------
    # Animation
    # ------------------------------------------------

    rotation = 0.0

    last_time = time.perf_counter()
    fps_timer = last_time

    frames = 0
    fps = 0.0

    # ------------------------------------------------
    # Main loop
    # ------------------------------------------------

    while not glfw.window_should_close(window):

        now = time.perf_counter()

        dt = now - last_time
        last_time = now

        # 30 degrees per second.
        rotation += 30.0 * dt

        # Keep angle small.
        if rotation >= 360.0:
            rotation -= 360.0

        # ------------------------------------------------
        # Clear
        # ------------------------------------------------

        glClearColor(
            1.0,
            1.0,
            1.0,
            1.0
        )

        glClear(GL_COLOR_BUFFER_BIT)

        # ------------------------------------------------
        # Model transform
        # ------------------------------------------------

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(
            framebuffer_width / 2,
            framebuffer_height / 2,
            0
        )

        glRotatef(
            rotation,
            0.0,
            0.0,
            1.0
        )

        # ------------------------------------------------
        # Draw image
        # ------------------------------------------------

        half = SQUARE_SIZE / 2

        glBindTexture(
            GL_TEXTURE_2D,
            texture
        )

        glBegin(GL_QUADS)

        glTexCoord2f(0.0, 0.0)
        glVertex2f(-half, -half)

        glTexCoord2f(1.0, 0.0)
        glVertex2f(half, -half)

        glTexCoord2f(1.0, 1.0)
        glVertex2f(half, half)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(-half, half)

        glEnd()

        glBindTexture(
            GL_TEXTURE_2D,
            0
        )

        # ------------------------------------------------
        # FPS
        # ------------------------------------------------

        frames += 1

        if now - fps_timer >= 1.0:

            fps = frames / (now - fps_timer)

            print(f"FPS: {fps:.1f}")

            frames = 0
            fps_timer = now

        glfw.set_window_title(
            window,
            f"OpenGL Rotating Image - {fps:.1f} FPS"
        )

        # ------------------------------------------------
        # Present
        # ------------------------------------------------

        glfw.swap_buffers(window)
        glfw.poll_events()

    # ------------------------------------------------
    # Cleanup
    # ------------------------------------------------

    glDeleteTextures([texture])

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
