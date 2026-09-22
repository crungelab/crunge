"""Flutter-style buttons.

A button is a padded, centered container around a single child. Size comes
from the child plus padding: the child measures itself, yoga adds the
padding, and the button only draws its own background and border. Label,
icon or a Row of both -- the button doesn't care what the child is.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Callable, ClassVar

from loguru import logger

from crunge import skia
from crunge import sdl
from crunge import yoga
from crunge.yoga.style_builder import StyleBuilder

from ..widget import Widget
from ..renderer import Renderer
from ..cursors import CURSOR_HAND, CURSOR_ARROW
from ..colors import Color, WHITE  # ASSUMPTION: module path
from .flex import EdgeInsets


# -- style ---------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class ButtonStyle:
    """None means draw nothing for that state."""

    background: Color | None = None
    hover: Color | None = None
    pressed: Color | None = None
    border: Color | None = None
    border_width: float = 1.0
    padding: EdgeInsets = EdgeInsets.symmetric(horizontal=16, vertical=8)


# Color is an immutable NamedTuple, so it keys the caches directly: buttons
# sharing a color share one Paint.

@cache
def _fill_paint(color: Color) -> skia.Paint:
    paint = skia.Paint()
    paint.set_color(color.to_argb_int())
    return paint


@cache
def _stroke_paint(color: Color, width: float) -> skia.Paint:
    paint = skia.Paint()
    paint.set_color(color.to_argb_int())
    paint.set_stroke(True)  # ASSUMPTION: SkPaint::setStroke is bound
    paint.set_stroke_width(width)
    return paint


# -- base ----------------------------------------------------------------------

class Button(Widget):
    """Plain button; keeps the look of the old text-only Button."""

    default_style: ClassVar[ButtonStyle] = ButtonStyle(
        background=Color.from_hex("#23272a"),
        hover=Color.from_hex("#2563eb"),
        pressed=Color.from_hex("#1d4ed8"),
    )

    def __init__(
        self,
        child: Widget,
        on_pressed: Callable[[], None] | None = None,
        *,
        button_style: ButtonStyle | None = None,
        style: yoga.Style | None = None,
        **kwargs,
    ) -> None:
        # Raise-first: old call sites passed a string as the first argument.
        if isinstance(child, str):
            raise TypeError(
                f"{type(self).__name__} takes a child widget now: "
                f"{type(self).__name__}(Text({child!r}), on_pressed=...)"
            )

        self.button_style = button_style or self.default_style
        b = (
            StyleBuilder(style)
            .justify_content(yoga.Justify.CENTER)
            .align_items(yoga.Align.CENTER)
        )
        self.button_style.padding.apply(b)
        super().__init__(style=b.build(), children=[child], **kwargs)

        self.on_pressed = on_pressed
        self.pressed = False

    @property
    def enabled(self) -> bool:
        """Flutter's rule: no callback means disabled."""
        return self.on_pressed is not None

    @property
    def cursor(self):
        return CURSOR_HAND if self.enabled else None

    # -- drawing -----------------------------------------------------------

    def _fill_color(self) -> Color | None:
        s = self.button_style
        if not self.enabled:
            return s.background
        if self.pressed and self.hovered and s.pressed is not None:
            return s.pressed
        if self.hovered and s.hover is not None:
            return s.hover
        return s.background

    def _draw(self) -> None:
        # ASSUMPTION: Node.draw() calls _draw() before drawing children, so
        # the background lands under the child.
        canvas = Renderer.get_current().canvas
        position = self.global_position
        size = self.size
        rect = skia.Rect(position.x, position.y, size.x, size.y)  # binding's Rect is XYWH

        fill = self._fill_color()
        if fill is not None:
            canvas.draw_rect(rect, _fill_paint(fill))

        s = self.button_style
        if s.border is not None:
            canvas.draw_rect(rect, _stroke_paint(s.border, s.border_width))

    # -- events ------------------------------------------------------------

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if not self.enabled or event.button != 1:  # left button only
            return False

        inside = self.hit_test(event.x, event.y)
        if event.down:
            self.pressed = inside
            return inside

        # Fire on release inside, like Flutter: dragging off cancels.
        was_pressed = self.pressed
        self.pressed = False
        if was_pressed and inside:
            logger.debug(f"{type(self).__name__} pressed at ({event.x}, {event.y})")
            self.on_pressed()
            return True
        return False


# -- variants --------------------------------------------------------------------

class FilledButton(Button):
    """High emphasis: solid accent fill."""

    default_style = ButtonStyle(
        background=Color.from_hex("#2563eb"),
        hover=Color.from_hex("#3b82f6"),
        pressed=Color.from_hex("#1d4ed8"),
    )


class OutlinedButton(Button):
    """Medium emphasis: border, fill only on interaction."""

    default_style = ButtonStyle(
        hover=WHITE.with_alpha(0.1),
        pressed=WHITE.with_alpha(0.2),
        border=Color.from_hex("#6b7280"),
    )


class TextButton(Button):
    """Low emphasis: no fill or border until hovered."""

    default_style = ButtonStyle(
        hover=WHITE.with_alpha(0.1),
        pressed=WHITE.with_alpha(0.2),
        padding=EdgeInsets.symmetric(horizontal=8, vertical=4),
    )