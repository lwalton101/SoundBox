import pyray as rl


def draw_textured_quad(texture, width, height):
    w = width / 2
    h = height / 2

    rl.rl_set_texture(texture.id)
    rl.rl_begin(rl.RL_TRIANGLES)

    rl.rl_color4ub(255, 255, 255, 255)

    # Front
    rl.rl_tex_coord2f(0, 0)
    rl.rl_vertex3f(-w, h, 0)

    rl.rl_tex_coord2f(1, 0)
    rl.rl_vertex3f(w, h, 0)

    rl.rl_tex_coord2f(1, 1)
    rl.rl_vertex3f(w, -h, 0)

    rl.rl_tex_coord2f(0, 0)
    rl.rl_vertex3f(-w, h, 0)

    rl.rl_tex_coord2f(1, 1)
    rl.rl_vertex3f(w, -h, 0)

    rl.rl_tex_coord2f(0, 1)
    rl.rl_vertex3f(-w, -h, 0)

    # Back
    # Reverse winding so the back is also visible.
    rl.rl_tex_coord2f(0, 0)
    rl.rl_vertex3f(w, h, 0)

    rl.rl_tex_coord2f(1, 0)
    rl.rl_vertex3f(-w, h, 0)

    rl.rl_tex_coord2f(1, 1)
    rl.rl_vertex3f(-w, -h, 0)

    rl.rl_tex_coord2f(0, 0)
    rl.rl_vertex3f(w, h, 0)

    rl.rl_tex_coord2f(1, 1)
    rl.rl_vertex3f(-w, -h, 0)

    rl.rl_tex_coord2f(0, 1)
    rl.rl_vertex3f(w, -h, 0)

    rl.rl_end()

    rl.rl_set_texture(0)


rl.init_window(1000, 700, "3D Card")
rl.set_target_fps(60)

texture = rl.load_texture("assets/hamilton.jpg")

camera = rl.Camera3D(
    rl.Vector3(0, 0, 6),
    rl.Vector3(0, 0, 0),
    rl.Vector3(0, 1, 0),
    45,
    rl.CAMERA_PERSPECTIVE
)

rotation = 0.0

while not rl.window_should_close():

    rotation += 60.0 * rl.get_frame_time()

    rl.begin_drawing()
    rl.clear_background(rl.DARKGRAY)

    rl.begin_mode_3d(camera)

    rl.rl_push_matrix()

    rl.rl_rotatef(rotation, 0, 1, 0)

    draw_textured_quad(texture, 4.0, 4.0)

    rl.rl_pop_matrix()

    rl.end_mode_3d()

    rl.end_drawing()


rl.unload_texture(texture)
rl.close_window()
