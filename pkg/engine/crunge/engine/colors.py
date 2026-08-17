from __future__ import annotations

from typing import Final, Iterable, NamedTuple

import glm

__all__ = [
    "Color",
    "NAMED_COLORS",
    "parse",
    "TRANSPARENT",
    "BLACK",
    "WHITE",
    "GRAY",
    "SILVER",
    "RED",
    "GREEN",
    "BLUE",
    "YELLOW",
    "CYAN",
    "MAGENTA",
    "ORANGE",
    "PURPLE",
    "PINK",
    "BROWN",
    "GOLD",
]


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055


class Color(NamedTuple):
    """Non-linear (sRGB) RGBA, components nominally 0..1.

    Immutable and hashable, so instances are safe to share as constants and
    to use as dict/cache keys.

    Values are deliberately not clamped -- components above 1.0 are meaningful
    for emissive and HDR use. Clamping happens only at byte/int conversion.

    Arithmetic is component-wise, not tuple-like: ``a + b`` adds channels
    rather than concatenating, and ``a * b`` modulates rather than repeating.
    """

    r: float
    g: float
    b: float
    a: float = 1.0

    # --- construction ---------------------------------------------------

    @classmethod
    def from_bytes(cls, r: int, g: int, b: int, a: int = 255) -> Color:
        return cls(r / 255.0, g / 255.0, b / 255.0, a / 255.0)

    @classmethod
    def from_argb_int(cls, value: int) -> Color:
        return cls.from_bytes(
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF,
            (value >> 24) & 0xFF,
        )

    @classmethod
    def from_rgba_int(cls, value: int) -> Color:
        return cls.from_bytes(
            (value >> 24) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF,
        )

    @classmethod
    def from_hex(cls, text: str) -> Color:
        """CSS ordering: #RGB, #RGBA, #RRGGBB, #RRGGBBAA."""
        s = text.strip().lstrip("#")
        if len(s) in (3, 4):
            s = "".join(c * 2 for c in s)
        if len(s) == 6:
            s += "ff"
        if len(s) != 8:
            raise ValueError(f"Invalid hex color: {text!r}")
        try:
            return cls.from_bytes(*(int(s[i : i + 2], 16) for i in range(0, 8, 2)))
        except ValueError:
            raise ValueError(f"Invalid hex color: {text!r}") from None

    @classmethod
    def from_argb_hex(cls, text: str) -> Color:
        """Tiled/Qt ordering: #AARRGGBB or #RRGGBB."""
        s = text.strip().lstrip("#")
        if len(s) == 6:
            s = "ff" + s
        if len(s) != 8:
            raise ValueError(f"Invalid ARGB hex color: {text!r}")
        try:
            a, r, g, b = (int(s[i : i + 2], 16) for i in range(0, 8, 2))
        except ValueError:
            raise ValueError(f"Invalid ARGB hex color: {text!r}") from None
        return cls.from_bytes(r, g, b, a)

    @classmethod
    def from_vec4(cls, v: glm.vec4) -> Color:
        return cls(v.x, v.y, v.z, v.w)

    @classmethod
    def from_linear(cls, v: glm.vec4) -> Color:
        """Linear RGB -> sRGB. Alpha is already linear and passes through."""
        return cls(_linear_to_srgb(v.x), _linear_to_srgb(v.y), _linear_to_srgb(v.z), v.w)

    @classmethod
    def gray(cls, value: float, a: float = 1.0) -> Color:
        return cls(value, value, value, a)

    # --- operations -----------------------------------------------------

    def with_alpha(self, a: float) -> Color:
        return self._replace(a=a)

    def scaled_rgb(self, k: float) -> Color:
        """Brightness scale; alpha untouched."""
        return Color(self.r * k, self.g * k, self.b * k, self.a)

    def faded(self, k: float) -> Color:
        """Alpha scale; color untouched."""
        return self._replace(a=self.a * k)

    def lerp(self, other: Iterable[float], t: float) -> Color:
        return Color(*(x + (y - x) * t for x, y in zip(self, other)))

    def clamped(self) -> Color:
        return Color(*(min(1.0, max(0.0, c)) for c in self))

    def __mul__(self, other: Iterable[float]) -> Color:  # type: ignore[override]
        """Component-wise modulate (tint). Overrides tuple repetition."""
        r, g, b, a = other
        return Color(self.r * r, self.g * g, self.b * b, self.a * a)

    def __add__(self, other: Iterable[float]) -> Color:  # type: ignore[override]
        """Component-wise add. Overrides tuple concatenation."""
        r, g, b, a = other
        return Color(self.r + r, self.g + g, self.b + b, self.a + a)

    def __sub__(self, other: Iterable[float]) -> Color:
        r, g, b, a = other
        return Color(self.r - r, self.g - g, self.b - b, self.a - a)

    # --- conversion -----------------------------------------------------

    @property
    def rgb(self) -> glm.vec3:
        return glm.vec3(self.r, self.g, self.b)

    def to_vec4(self) -> glm.vec4:
        return glm.vec4(self.r, self.g, self.b, self.a)

    def to_linear(self) -> glm.vec4:
        """sRGB -> linear. Alpha is already linear and passes through."""
        return glm.vec4(
            _srgb_to_linear(self.r),
            _srgb_to_linear(self.g),
            _srgb_to_linear(self.b),
            self.a,
        )

    def premultiplied(self) -> Color:
        """Premultiply in sRGB space. Prefer premultiplied_linear for shader use."""
        return Color(self.r * self.a, self.g * self.a, self.b * self.a, self.a)

    def premultiplied_linear(self) -> glm.vec4:
        """Premultiply in linear space, which is where it is physically correct."""
        lin = self.to_linear()
        return glm.vec4(lin.x * lin.w, lin.y * lin.w, lin.z * lin.w, lin.w)

    def to_bytes(self) -> tuple[int, int, int, int]:
        r, g, b, a = (min(255, max(0, int(round(c * 255.0)))) for c in self)
        return (r, g, b, a)

    def to_argb_int(self) -> int:
        r, g, b, a = self.to_bytes()
        return (a << 24) | (r << 16) | (g << 8) | b

    def to_rgba_int(self) -> int:
        r, g, b, a = self.to_bytes()
        return (r << 24) | (g << 16) | (b << 8) | a

    def to_hex(self, include_alpha: bool = True) -> str:
        r, g, b, a = self.to_bytes()
        if include_alpha:
            return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
        return f"#{r:02x}{g:02x}{b:02x}"

    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


# --- named colors (sRGB, CSS-derived where applicable) ------------------

TRANSPARENT: Final = Color(0.0, 0.0, 0.0, 0.0)
BLACK: Final = Color(0.0, 0.0, 0.0)
WHITE: Final = Color(1.0, 1.0, 1.0)
GRAY: Final = Color.from_bytes(128, 128, 128)
SILVER: Final = Color.from_bytes(192, 192, 192)

RED: Final = Color(1.0, 0.0, 0.0)
GREEN: Final = Color(0.0, 1.0, 0.0)
BLUE: Final = Color(0.0, 0.0, 1.0)
YELLOW: Final = Color(1.0, 1.0, 0.0)
CYAN: Final = Color(0.0, 1.0, 1.0)
MAGENTA: Final = Color(1.0, 0.0, 1.0)

ORANGE: Final = Color.from_bytes(255, 165, 0)
PURPLE: Final = Color.from_bytes(128, 0, 128)
PINK: Final = Color.from_bytes(255, 192, 203)
BROWN: Final = Color.from_bytes(165, 42, 42)
GOLD: Final = Color.from_bytes(255, 215, 0)


NAMED_COLORS: dict[str, Color] = {
    "transparent": TRANSPARENT,
    "black": BLACK,
    "white": WHITE,
    "gray": GRAY,
    "grey": GRAY,
    "silver": SILVER,
    "red": RED,
    "green": GREEN,
    "blue": BLUE,
    "yellow": YELLOW,
    "cyan": CYAN,
    "aqua": CYAN,
    "magenta": MAGENTA,
    "fuchsia": MAGENTA,
    "orange": ORANGE,
    "purple": PURPLE,
    "pink": PINK,
    "brown": BROWN,
    "gold": GOLD,
}


def parse(text: str) -> Color:
    """Parse '#RGB', '#RGBA', '#RRGGBB', '#RRGGBBAA', or a registered name.

    Games may add entries to NAMED_COLORS to extend the recognized names.
    """
    s = text.strip()
    if s.startswith("#"):
        return Color.from_hex(s)
    try:
        return NAMED_COLORS[s.lower()]
    except KeyError:
        raise ValueError(f"Unknown color: {text!r}") from None