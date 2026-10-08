from pyray import Font, Image, Texture, load_font_ex, load_image, load_texture, unload_font, unload_image, unload_texture


class Textures:
    textures: dict[str, Texture] = {}
    accessed_this_frame: dict[str, bool] = {}

    @staticmethod
    def get_texture(texture_name: str) -> Texture:
        if texture_name not in Textures.textures.keys():
            texture = load_texture(f"assets/{texture_name}")
            Textures.textures[texture_name] = texture

        image = Textures.textures[texture_name]
        Textures.accessed_this_frame[texture_name] = True
        return image

    @staticmethod
    def clear_cached_images():
        # snapshot the keys so we're not mutating the dict while iterating it
        unused = [name for name in Textures.textures if name not in Textures.accessed_this_frame]

        for name in unused:
            texture = Textures.textures.pop(name, None)
            if texture is not None:
                unload_texture(texture)

        Textures.accessed_this_frame.clear()
