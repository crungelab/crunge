from . import (
    Style,
    Dimension,
    Align,
    FlexDirection,
    Wrap,
    Overflow,
    Display,
    PositionType,
    Direction,
    Edge,
    StyleSizeLength,
    StyleLength,
)


class StyleBuilder:
    def __init__(self):
        self.style = Style()

    def flex_grow(self, value):
        self.style.set_flex_grow(value)
        return self

    def flex_shrink(self, value):
        self.style.set_flex_shrink(value)
        return self

    def flex_basis(self, value):
        self.style.set_flex_basis(value)
        return self

    def dimension(self, dimension, value):
        self.style.set_dimension(dimension, value)
        return self

    def width(self, value):
        self.dimension(Dimension.WIDTH, StyleSizeLength.points(value))
        return self

    def height(self, value):
        self.dimension(Dimension.HEIGHT, StyleSizeLength.points(value))
        return self

    def size(self, width, height):
        self.width(width)
        self.height(height)
        return self

    def margin(self, edge, value):
        #self.style.set_margin(edge, value)
        self.style.set_margin(edge, StyleLength.points(value))
        return self

    def padding(self, edge, value):
        self.style.set_padding(edge, value)
        return self

    def border(self, edge, value):
        self.style.set_border(edge, value)
        return self

    def position(self, edge, value):
        self.style.set_position(edge, value)
        return self

    def align_items(self, value):
        self.style.set_align_items(value)
        return self

    def align_self(self, value):
        self.style.set_align_self(value)
        return self

    def align_content(self, value):
        self.style.set_align_content(value)
        return self

    def flex_direction(self, value):
        self.style.set_flex_direction(value)
        return self

    def flex_wrap(self, value):
        self.style.set_flex_wrap(value)
        return self

    def justify_content(self, value):
        self.style.set_justify_content(value)
        return self

    def overflow(self, value):
        self.style.set_overflow(value)
        return self

    def display(self, value):
        self.style.set_display(value)
        return self

    def aspect_ratio(self, value):
        self.style.set_aspect_ratio(value)
        return self

    def max_dimension(self, dimension, value):
        self.style.set_max_dimension(dimension, value)
        return self

    def min_dimension(self, dimension, value):
        self.style.set_min_dimension(dimension, value)
        return self

    def position_type(self, value):
        self.style.set_position_type(value)
        return self

    def direction(self, value):
        self.style.set_direction(value)
        return self

    def wrap_before(self, value):
        self.style.set_wrap_before(value)
        return self

    def z_index(self, value):
        self.style.set_z_index(value)
        return self

    def max_height(self, value):
        self.style.set_max_height(value)
        return self

    def max_width(self, value):
        self.style.set_max_width(value)
        return self

    def min_height(self, value):
        self.style.set_min_height(value)
        return self

    def min_width(self, value):
        self.style.set_min_width(value)
        return self

    def gap(self, value):
        self.style.set_gap(value)
        return self

    def row_gap(self, value):
        self.style.set_row_gap(value)
        return self

    def column_gap(self, value):
        self.style.set_column_gap(value)
        return self

    def build(self):
        return self.style
