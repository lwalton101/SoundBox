from typing import override

from pyray import WHITE, Color, Vector2, draw_text_pro, measure_text_ex

from ui.WindowState import WindowState
from ui.fonts import Fonts
from ui.widget.Widget import Widget


class TextWidget(Widget):
    LARGE_SIZE: int = 50
    MEDIUM_SIZE: int = 32
    SMALL_SIZE: int = 24

    def __init__(
        self,
        state: WindowState,
        x: float,
        y: float,
        font_size: int = LARGE_SIZE,
        spacing: int = -2,
        text: str = "test text",
        color: Color = WHITE,
        centered: bool = False,
        max_width: float | None = None,
        line_spacing: float = 0,
    ) -> None:
        super().__init__(state, x, y)
        self.font_size = font_size
        self.spacing = spacing
        self.text = text
        self.color = color
        self.centered = centered
        self.max_width = max_width      # None = no wrapping
        self.line_spacing = line_spacing  # extra pixels between lines
        self.font = Fonts.get_font("RobotoMono", self.font_size)

        self._cache_key: tuple | None = None
        self._cache_lines: list[str] = []

    # ---------- measuring / wrapping ----------

    def _width(self, text: str) -> float:
        return measure_text_ex(self.font, text, self.font_size, self.spacing).x

    def _line_height(self) -> float:
        return measure_text_ex(self.font, "Ag", self.font_size, self.spacing).y + self.line_spacing

    def _wrap(self) -> list[str]:
        if self.max_width is None:
            return self.text.split("\n")

        lines: list[str] = []
        for paragraph in self.text.split("\n"):
            current = ""
            for word in paragraph.split(" "):
                candidate = f"{current} {word}" if current else word
                if self._width(candidate) <= self.max_width:
                    current = candidate
                    continue

                # candidate doesn't fit: flush the current line
                if current:
                    lines.append(current)
                    current = ""

                if self._width(word) <= self.max_width:
                    current = word
                else:
                    # single word too long for a line: break it by character
                    for ch in word:
                        if current and self._width(current + ch) > self.max_width:
                            lines.append(current)
                            current = ch
                        else:
                            current += ch
            lines.append(current)
        return lines

    def get_lines(self) -> list[str]:
        """Wrapped lines, recomputed only when inputs change."""
        self.font = Fonts.get_font("RobotoMono", self.font_size)
        key = (self.text, self.font_size, self.spacing, self.max_width)
        if key != self._cache_key:
            self._cache_key = key
            self._cache_lines = self._wrap()
        return self._cache_lines

    def get_text_dim(self) -> Vector2:
        lines = self.get_lines()
        width = max((self._width(line) for line in lines), default=0)
        height = self._line_height() * len(lines)
        return Vector2(width, height)

    # ---------- drawing ----------

    @override
    def draw(self, x: float, y: float):
        lines = self.get_lines()
        line_h = self._line_height()

        if self.centered:
            y -= line_h * len(lines) / 2

        for i, line in enumerate(lines):
            line_x = x
            if self.centered:
                line_x -= self._width(line) / 2  # center each line individually
            draw_text_pro(
                self.font, line, (line_x, y + i * line_h),
                (0, 0), 0, self.font_size, self.spacing, self.color,
            )