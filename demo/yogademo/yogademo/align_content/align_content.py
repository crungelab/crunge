import math

from loguru import logger

from crunge import wgpu
from crunge import skia
from crunge import yoga

from ..common import Demo, Renderer


class AlignContentDemo(Demo):
    def __init__(self):
        super().__init__()
        # Create a root node
        self.root = root = yoga.Layout()
        root.set_width(200)
        root.set_height(250)
        root.set_padding(yoga.Edge.ALL, 10)
        root.set_align_content(yoga.Align.FLEX_START)
        root.set_flex_wrap(yoga.Wrap.WRAP)

        for i in range(5):
            child = yoga.Layout()
            child.set_width(50)
            child.set_height(50)
            child.set_margin(yoga.Edge.ALL, 5)
            root.add_child(child)

        # Calculate layout for the root node
        # root.calculate_layout(width=100, height=100)
        # yoga.calculate_layout(root, 100, 100, yoga.Direction.LTR)
        root.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)

        self.debug_layout(root)

    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            # paint = skia.Paint()
            # paint.set_color(0xFFFFFFFF)
            # canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
            self.render_node(self.root, canvas)

    def render_node(self, node: yoga.Layout, canvas: skia.Canvas, depth=0, max_depth=6):
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
            self.render_node(child, canvas, depth=depth + 1, max_depth=max_depth)


def main():
    AlignContentDemo().run()


if __name__ == "__main__":
    main()
