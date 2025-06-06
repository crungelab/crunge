import math

from loguru import logger

from crunge import wgpu
from crunge import skia
from crunge import yoga

from ..common import Demo, Renderer


class FlexColumnDemo(Demo):
    def __init__(self):
        super().__init__()
        self.text_paint = text_paint = skia.Paint()
        text_paint.set_color(0xFFFF00FF)
        self.font = font = skia.Font()
        font.set_size(16)

        # Create a root node
        root_style = yoga.Style()

        root_style.set_flex_direction(yoga.FlexDirection.COLUMN)
        root_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(512))
        root_style.set_dimension(
            yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(512)
        )
        root_style.set_padding(yoga.Edge.ALL, yoga.StyleLength.points(32))

        self.root = root = yoga.Layout()
        root.set_style(root_style)

        child0 = yoga.Layout()
        child0_style = yoga.Style()
        child0_style.set_flex_grow(.25)
        child0_style.set_margin(yoga.Edge.BOTTOM, yoga.StyleLength.points(10))

        child0.set_style(child0_style)
        #child0.set_height(50)

        root.add_child(child0)

        child1 = yoga.Layout()
        child1_style = yoga.Style()
        child1_style.set_flex_grow(0.75)

        child1.set_style(child1_style)
        #child1.set_height(50)

        root.add_child(child1)

        # Calculate layout for the root node
        #root.calculate_layout(math.nan, math.nan, yoga.Direction.LTR)
        root.calculate_bounds(256, 256, yoga.Direction.LTR)

        self.debug_layout(root)

    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            self.render_layout(self.root, canvas)

    def render_layout(self, node: yoga.Layout, canvas: skia.Canvas, depth=0, max_depth=6):
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

        canvas.draw_string(f"Node {depth}", left + 5, top + 15, self.font, self.text_paint)

        for child in node.children:
            self.render_layout(child, canvas, depth=depth + 1, max_depth=max_depth)


def main():
    FlexColumnDemo().run()


if __name__ == "__main__":
    main()
