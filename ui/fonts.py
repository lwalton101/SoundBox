from pyray import Font, load_font_ex


class Fonts:
    fonts: dict[str, dict[int, Font]] = {}

    @staticmethod
    def get_font(font_name: str, font_size: int) -> Font:
        if font_name not in Fonts.fonts.keys():
            font = load_font_ex(f"assets/{font_name}.ttf", font_size, None, 255)
            Fonts.fonts[font_name] = {font_size: font}
            return font

        if font_size not in Fonts.fonts[font_name].keys():
            font = load_font_ex(f"assets/{font_name}.ttf", font_size, None, 255)
            Fonts.fonts[font_name][font_size] = font
            return font

        return Fonts.fonts[font_name][font_size]
