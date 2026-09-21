"""Flutter-flavored layout widgets.

Style presets, not layout algorithms: each class builds a yoga.Style and
hands it to Widget, whose Layout chip does the work. Nothing here
overrides on_layout or touches geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from crunge import yoga
from crunge.yoga.style_builder import StyleBuilder  # ASSUMPTION: module path

from ..widget import Widget

# -- enums -------------------------------------------------------------------


class MainAxisAlignment(Enum):
    # ASSUMPTION: Justify is bound with the same UPPER_CASE naming as Align
    START = yoga.Justify.FLEX_START
    END = yoga.Justify.FLEX_END
    CENTER = yoga.Justify.CENTER
    SPACE_BETWEEN = yoga.Justify.SPACE_BETWEEN
    SPACE_AROUND = yoga.Justify.SPACE_AROUND
    SPACE_EVENLY = yoga.Justify.SPACE_EVENLY


class CrossAxisAlignment(Enum):
    START = yoga.Align.FLEX_START
    END = yoga.Align.FLEX_END
    CENTER = yoga.Align.CENTER
    STRETCH = yoga.Align.STRETCH
    BASELINE = yoga.Align.BASELINE


@dataclass(frozen=True, slots=True)
class EdgeInsets:
    left: float = 0.0
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0

    @classmethod
    def all(cls, v: float) -> EdgeInsets:
        return cls(v, v, v, v)

    @classmethod
    def symmetric(cls, *, horizontal: float = 0.0, vertical: float = 0.0) -> EdgeInsets:
        return cls(horizontal, vertical, horizontal, vertical)

    def apply(self, b: StyleBuilder) -> StyleBuilder:
        points = yoga.StyleLength.points
        return (
            b.padding(yoga.Edge.LEFT, points(self.left))
            .padding(yoga.Edge.TOP, points(self.top))
            .padding(yoga.Edge.RIGHT, points(self.right))
            .padding(yoga.Edge.BOTTOM, points(self.bottom))
        )


# -- flex containers -----------------------------------------------------------


class Flex(Widget):
    """Presets are applied on top of `style`, so callers can still size,
    pad or position the container through a StyleBuilder."""

    def __init__(
        self,
        direction: yoga.FlexDirection,
        children: list[Widget] | None = None,
        *,
        main_axis_alignment: MainAxisAlignment = MainAxisAlignment.START,
        cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.STRETCH,  # Yoga's default, not Flutter's
        spacing: float = 0.0,
        wrap: bool = False,
        style: yoga.Style | None = None,
        priority: int = 0,
    ) -> None:
        b = (
            StyleBuilder(style)
            .flex_direction(direction)
            .justify_content(main_axis_alignment.value)
            .align_items(cross_axis_alignment.value)
            .flex_wrap(yoga.Wrap.WRAP if wrap else yoga.Wrap.NO_WRAP)
        )
        if spacing:
            b.gap(
                yoga.StyleLength.points(spacing)
            )  # ASSUMPTION: set_gap takes a StyleLength
        super().__init__(style=b.build(), priority=priority, children=children)


class Row(Flex):
    def __init__(
        self, children: list[Widget] | None = None, *, reverse: bool = False, **kwargs
    ) -> None:
        direction = (
            yoga.FlexDirection.ROW_REVERSE if reverse else yoga.FlexDirection.ROW
        )
        super().__init__(direction, children, **kwargs)


class Column(Flex):
    def __init__(
        self, children: list[Widget] | None = None, *, reverse: bool = False, **kwargs
    ) -> None:
        direction = (
            yoga.FlexDirection.COLUMN_REVERSE if reverse else yoga.FlexDirection.COLUMN
        )
        super().__init__(direction, children, **kwargs)


# -- child modifiers -------------------------------------------------------------
#
# In Flutter these are wrapper widgets. Here flex participation is style on
# the child itself, so they edit the child and return it -- no extra node.
# Read-modify-write through Widget.style so it works whether the binding's
# get_style returns a reference or a copy.


def expanded[W: Widget](child: W, flex: float = 1.0) -> W:
    """Take a `flex` share of the parent's main axis, ignoring content size."""
    child.style = (
        StyleBuilder(child.style)
        .flex_grow(flex)
        .flex_shrink(1.0)
        .flex_basis(
            yoga.StyleSizeLength.points(0)
        )  # ASSUMPTION: set_flex_basis takes a StyleSizeLength
        .build()
    )
    return child


# -- leaf / single-child boxes ------------------------------------------------------


class Spacer(Widget):
    def __init__(self, flex: float = 1.0) -> None:
        super().__init__()
        expanded(self, flex)


class SizedBox(Widget):
    def __init__(
        self,
        width: float | None = None,
        height: float | None = None,
        child: Widget | None = None,
    ) -> None:
        b = StyleBuilder()
        if width is not None:
            b.width(width)
        if height is not None:
            b.height(height)
        super().__init__(style=b.build(), children=[child] if child else None)


class Padding(Widget):
    def __init__(self, padding: EdgeInsets, child: Widget) -> None:
        super().__init__(style=padding.apply(StyleBuilder()).build(), children=[child])


class Center(Widget):
    """Fills the parent and centers its child on both axes."""

    def __init__(self, child: Widget) -> None:
        style = (
            StyleBuilder()
            .flex_grow(1.0)
            .align_self(yoga.Align.STRETCH)
            .justify_content(yoga.Justify.CENTER)
            .align_items(yoga.Align.CENTER)
            .build()
        )
        super().__init__(style=style, children=[child])
