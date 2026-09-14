from pyray import Font, load_font_ex, unload_font


class Fonts:
    fonts: dict[str, dict[int, Font]] = {}
    accessed_this_frame: dict[Font, bool] = {}

    @staticmethod
    def get_font(font_name: str, font_size: int) -> Font:
        if font_name not in Fonts.fonts.keys():
            font = load_font_ex(f"assets/{font_name}.ttf", font_size, None, 255)
            Fonts.fonts[font_name] = {font_size: font}

        if font_size not in Fonts.fonts[font_name].keys():
            font = load_font_ex(f"assets/{font_name}.ttf", font_size, None, 255)
            Fonts.fonts[font_name][font_size] = font

        font = Fonts.fonts[font_name][font_size]
        Fonts.accessed_this_frame[font] = True
        return font

    @staticmethod
    def clear_cached_fonts():
        accessed = Fonts.accessed_this_frame

        for font_name, fonts_by_size in Fonts.fonts.items():
            for font_size, font in list(fonts_by_size.items()):
                if font in accessed:
                    continue

                del fonts_by_size[font_size]
                unload_font(font)

        accessed.clear()
