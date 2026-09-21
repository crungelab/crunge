"""Fluent builder for yoga.Style.

Lengths take a bare number, meaning points, or an explicit StyleLength /
StyleSizeLength for percent, auto and the rest -- the same rule for every
method, so `.padding(Edge.ALL, 32)` and `.margin(Edge.ALL, 32)` behave alike.

Every method returns the builder. `build()` returns the Style being edited,
not a copy: a builder seeded with an existing style edits it in place.
"""
from __future__ import annotations

from typing import Self

from . import (
    Align,
    Dimension,
    Direction,
    Display,
    Edge,
    FlexDirection,
    Gutter,
    Justify,
    Overflow,
    PositionType,
    Style,
    StyleLength,
    StyleSizeLength,
    Wrap,
)

type Length = float | StyleLength
type SizeLength = float | StyleSizeLength


def _length(value: Length) -> StyleLength:
    if isinstance(value, StyleLength):
        return value
    return StyleLength.points(value)


def _size_length(value: SizeLength) -> StyleSizeLength:
    if isinstance(value, StyleSizeLength):
        return value
    return StyleSizeLength.points(value)


class StyleBuilder:
    def __init__(self, style: Style | None = None) -> None:
        self.style = style if style is not None else Style()

    def build(self) -> Style:
        return self.style

    # -- flex item ---------------------------------------------------------

    def flex(self, value: float) -> Self:
        self.style.set_flex(value)
        return self

    def flex_grow(self, value: float) -> Self:
        self.style.set_flex_grow(value)
        return self

    def flex_shrink(self, value: float) -> Self:
        self.style.set_flex_shrink(value)
        return self

    def flex_basis(self, value: SizeLength) -> Self:
        self.style.set_flex_basis(_size_length(value))
        return self

    def align_self(self, value: Align) -> Self:
        self.style.set_align_self(value)
        return self

    # -- flex container ----------------------------------------------------

    def direction(self, value: Direction) -> Self:
        self.style.set_direction(value)
        return self

    def flex_direction(self, value: FlexDirection) -> Self:
        self.style.set_flex_direction(value)
        return self

    def flex_wrap(self, value: Wrap) -> Self:
        self.style.set_flex_wrap(value)
        return self

    def justify_content(self, value: Justify) -> Self:
        self.style.set_justify_content(value)
        return self

    def align_items(self, value: Align) -> Self:
        self.style.set_align_items(value)
        return self

    def align_content(self, value: Align) -> Self:
        self.style.set_align_content(value)
        return self

    def gap(self, value: Length, gutter: Gutter = Gutter.ALL) -> Self:
        self.style.set_gap(gutter, _length(value))
        return self

    def row_gap(self, value: Length) -> Self:
        return self.gap(value, Gutter.ROW)

    def column_gap(self, value: Length) -> Self:
        return self.gap(value, Gutter.COLUMN)

    # -- box model ---------------------------------------------------------

    def margin(self, edge: Edge, value: Length) -> Self:
        self.style.set_margin(edge, _length(value))
        return self

    def padding(self, edge: Edge, value: Length) -> Self:
        self.style.set_padding(edge, _length(value))
        return self

    def border(self, edge: Edge, value: Length) -> Self:
        self.style.set_border(edge, _length(value))
        return self

    # -- dimensions --------------------------------------------------------

    def dimension(self, dimension: Dimension, value: SizeLength) -> Self:
        self.style.set_dimension(dimension, _size_length(value))
        return self

    def width(self, value: SizeLength) -> Self:
        return self.dimension(Dimension.WIDTH, value)

    def height(self, value: SizeLength) -> Self:
        return self.dimension(Dimension.HEIGHT, value)

    def size(self, width: SizeLength, height: SizeLength) -> Self:
        return self.width(width).height(height)

    def width_percent(self, value: float) -> Self:
        return self.width(StyleSizeLength.percent(value))

    def height_percent(self, value: float) -> Self:
        return self.height(StyleSizeLength.percent(value))

    def size_percent(self, width: float, height: float) -> Self:
        return self.width_percent(width).height_percent(height)

    def min_dimension(self, dimension: Dimension, value: SizeLength) -> Self:
        self.style.set_min_dimension(dimension, _size_length(value))
        return self

    def max_dimension(self, dimension: Dimension, value: SizeLength) -> Self:
        self.style.set_max_dimension(dimension, _size_length(value))
        return self

    def min_width(self, value: SizeLength) -> Self:
        return self.min_dimension(Dimension.WIDTH, value)

    def min_height(self, value: SizeLength) -> Self:
        return self.min_dimension(Dimension.HEIGHT, value)

    def max_width(self, value: SizeLength) -> Self:
        return self.max_dimension(Dimension.WIDTH, value)

    def max_height(self, value: SizeLength) -> Self:
        return self.max_dimension(Dimension.HEIGHT, value)

    def aspect_ratio(self, value: float) -> Self:
        self.style.set_aspect_ratio(value)
        return self

    # -- positioning -------------------------------------------------------

    def position_type(self, value: PositionType) -> Self:
        self.style.set_position_type(value)
        return self

    def position(self, edge: Edge, value: Length) -> Self:
        self.style.set_position(edge, _length(value))
        return self

    # -- misc --------------------------------------------------------------

    def overflow(self, value: Overflow) -> Self:
        self.style.set_overflow(value)
        return self

    def display(self, value: Display) -> Self:
        self.style.set_display(value)
        return self