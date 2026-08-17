from __future__ import annotations

from typing import Iterable, NamedTuple

import glm


class Color(NamedTuple):
    """Non-linear (sRGB) RGBA, components nominally 0..1.

    Values are deliberately not clamped — >1.0 is meaningful for emissive/HDR.
    Clamping happens only at byte/int conversion boundaries.
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
            (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF, (value >> 24) & 0xFF
        )

    @classmethod
    def from_rgba_int(cls, value: int) -> Color:
        return cls.from_bytes(
            (value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF
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
        return cls.from_bytes(*(int(s[i : i + 2], 16) for i in range(0, 8, 2)))

    @classmethod
    def from_argb_hex(cls, text: str) -> Color:
        """Tiled/Qt ordering: #AARRGGBB or #RRGGBB."""
        s = text.strip().lstrip("#")
        if len(s) == 6:
            s = "ff" + s
        if len(s) != 8:
            raise ValueError(f"Invalid ARGB hex color: {text!r}")
        a, r, g, b = (int(s[i : i + 2], 16) for i in range(0, 8, 2))
        return cls.from_bytes(r, g, b, a)

    @classmethod
    def from_vec4(cls, v: glm.vec4) -> Color:
        return cls(v.x, v.y, v.z, v.w)

    # --- operations -----------------------------------------------------

    def with_alpha(self, a: float) -> Color:
        return self._replace(a=a)

    def scaled_rgb(self, k: float) -> Color:
        """Brightness scale, alpha untouched."""
        return Color(self.r * k, self.g * k, self.b * k, self.a)

    def lerp(self, other: Iterable[float], t: float) -> Color:
        return Color(*(x + (y - x) * t for x, y in zip(self, other)))

    def premultiplied(self) -> Color:
        return Color(self.r * self.a, self.g * self.a, self.b * self.a, self.a)

    def __mul__(self, other: Iterable[float]) -> Color:  # type: ignore[override]
        """Component-wise modulate (tint). Overrides tuple repetition."""
        r, g, b, a = other
        return Color(self.r * r, self.g * g, self.b * b, self.a * a)

    def __add__(self, other: Iterable[float]) -> Color:  # type: ignore[override]
        """Component-wise add. Overrides tuple concatenation."""
        r, g, b, a = other
        return Color(self.r + r, self.g + g, self.b + b, self.a + a)

    # --- conversion -----------------------------------------------------

    def to_vec4(self) -> glm.vec4:
        return glm.vec4(self.r, self.g, self.b, self.a)

    def to_vec3(self) -> glm.vec3:
        return glm.vec3(self.r, self.g, self.b)

    def to_bytes(self) -> tuple[int, int, int, int]:
        return tuple(min(255, max(0, int(round(c * 255.0)))) for c in self)  # type: ignore

    def to_argb_int(self) -> int:
        r, g, b, a = self.to_bytes()
        return (a << 24) | (r << 16) | (g << 8) | b

    def to_rgba_int(self) -> int:
        r, g, b, a = self.to_bytes()
        return (r << 24) | (g << 16) | (b << 8) | a

    def to_linear(self) -> glm.vec4:
        """sRGB -> linear. Alpha is already linear and passes through."""
        return glm.vec4(*(_srgb_to_linear(c) for c in (self.r, self.g, self.b)), self.a)


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055
