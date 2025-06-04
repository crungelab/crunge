import math

from loguru import logger

from crunge import skia
from crunge import yoga

from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page



class TreePage(Page):
    def reset(self):
        super().reset()
        # Create a root node
        """
        root_style = yoga.Style()

        root_style.set_flex_direction(yoga.FlexDirection.ROW)
        # root_style.set_align_items(yoga.Align.CENTER)
        root_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        # style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(math.nan))
        root_style.set_dimension(
            yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(100)
        )
        # style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(math.nan))

        self.root = root = yoga.Node()
        root.set_style(root_style)
        """
        self.root = root = yoga.Layout()
        root.set_style(
            yoga.StyleBuilder()
            #.flex_direction(yoga.FlexDirection.ROW)
            .flex_direction(yoga.FlexDirection.COLUMN)
            #.align_items(yoga.Align.CENTER)
            .width(256)
            .height(256)
            .build()
        )

        child0 = yoga.Layout()
        child0_style = yoga.Style()
        child0_style.set_flex_grow(1.0)
        # child0_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        # child0_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(20))
        child0_style.set_margin(yoga.Edge.RIGHT, yoga.StyleLength.points(10))

        child0.set_style(child0_style)

        root.add_child(child0)

        child1 = yoga.Layout()
        child1_style = yoga.Style()
        # child1_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        # child1_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(10))
        child1_style.set_flex_grow(1.0)

        child1.set_style(child1_style)

        root.add_child(child1)

        # Calculate layout for the root node
        # root.calculate_layout(width=100, height=100)
        # yoga.calculate_layout(root, 100, 100, yoga.Direction.LTR)
        root.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)

        self.debug_layout(root)

    def draw(self, renderer: Renderer):
        #with self.canvas_target(renderer) as canvas:
        with renderer.canvas_target() as canvas:
            # paint = skia.Paint()
            # paint.set_color(0xFFFFFFFF)
            # canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
            self.draw_layout(self.root, canvas)
        super().draw(renderer)

    def draw_layout(self, node: yoga.Layout, canvas: skia.Canvas, depth=0, max_depth=6):
        bounds = node.get_computed_bounds()
        left = bounds.left
        top = bounds.top
        width = bounds.width
        height = bounds.height

        # Calculate shade of grey (darker at depth 0, lighter as depth increases)
        # Clamp depth so that we stay within 0 (black) to 255 (white)
        depth = min(depth, max_depth)
        shade = int(32 + (224 * depth // max_depth))  # 32 to 255
        color = (0xFF << 24) | (shade << 16) | (shade << 8) | shade  # ARGB

        paint = skia.Paint()
        paint.set_color(color)
        canvas.draw_rect(skia.Rect(left, top, width, height), paint)

        for child in node.children:
            self.draw_layout(child, canvas, depth=depth + 1, max_depth=max_depth)


def install(app: App):
    app.add_channel(PageChannel(TreePage, "tree", "Tree"))
