import math

from loguru import logger

from crunge import wgpu
from crunge import skia
from crunge import yoga

from ..common import Demo, Renderer


class TreeDemo(Demo):
    def __init__(self):
        super().__init__()
        # Create a root node
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

        child0 = yoga.Node()
        child0_style = yoga.Style()
        child0_style.set_flex_grow(1.0)
        # child0_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        # child0_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(20))
        child0_style.set_margin(yoga.Edge.RIGHT, yoga.StyleLength.points(10))

        child0.set_style(child0_style)

        root.add_child(child0)

        child1 = yoga.Node()
        child1_style = yoga.Style()
        # child1_style.set_dimension(yoga.Dimension.WIDTH, yoga.StyleSizeLength.points(100))
        # child1_style.set_dimension(yoga.Dimension.HEIGHT, yoga.StyleSizeLength.points(10))
        child1_style.set_flex_grow(1.0)

        child1.set_style(child1_style)

        root.add_child(child1)

        # Calculate layout for the root node
        # root.calculate_layout(width=100, height=100)
        # yoga.calculate_layout(root, 100, 100, yoga.Direction.LTR)
        root.calculate_layout(math.nan, math.nan, yoga.Direction.LTR)

        self.debug_node(root)

    def debug_node(self, node: yoga.Node):
        layout = node.get_computed_layout()
        left = layout.left
        top = layout.top
        width = layout.width
        height = layout.height
        print(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")
        for child in node.children:
            self.debug_node(child)

    def render(self, renderer: Renderer):
        with self.canvas_target() as canvas:
            # paint = skia.Paint()
            # paint.set_color(0xFFFFFFFF)
            # canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
            self.render_node(self.root, canvas)

    def render_node(self, node: yoga.Node, canvas: skia.Canvas, depth=0, max_depth=6):
        layout = node.get_computed_layout()
        left = layout.left
        top = layout.top
        width = layout.width
        height = layout.height

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
    TreeDemo().run()


if __name__ == "__main__":
    main()
