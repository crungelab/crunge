from loguru import logger

from crunge import skia
from crunge import yoga
from crunge.yoga.style_builder import StyleBuilder

from crunge.engine import Renderer, App
from crunge.engine.widget import Widget
from crunge.engine.ui.flex import Row, expanded, CrossAxisAlignment
from crunge.engine.ui import Text, Button
from crunge.engine.colors import Color, WHITE
from crunge.demo import PageChannel

from ..page import Page


class FlexRowPage(Page):
    def setup(self):
        super().setup()
        self.text_paint = text_paint = skia.Paint()
        text_paint.set_color(0xFFFF00FF)
        self.font = font = skia.Font()
        font.set_size(16)

        self.root = Row(
            [
                Text("Hello", color=WHITE),
                Text("World", color=WHITE),
                Text("Again", color=WHITE),
            ],
            spacing=10,
            cross_axis_alignment=CrossAxisAlignment.CENTER,
            style=(
                StyleBuilder()
                .size(512, 512)
                .padding(yoga.Edge.ALL, 32)
                .build()
            ),
        ).create()

        # Layout chips link yoga's tree in plug/on_added. If these widgets
        # never go through the chip lifecycle, the root has no yoga children
        # and the row computes empty -- say so rather than draw a blank page.
        linked = self.root.layout.layout_node.get_child_count()
        if linked != len(self.root.children):
            logger.warning(
                f"FlexRowPage: {linked} of {len(self.root.children)} "
                "children linked into yoga; chip lifecycle has not run"
            )

        # Root is explicitly sized, so leave the available space as nan and
        # let the style decide.
        self.root.layout.calculate()
        # Push results through on_layout so Widget.position/size are real --
        # drawing below reads widgets, not yoga nodes.
        self.root.layout.apply()

        self.debug_layout(self.root.layout.layout_node)

    def _draw(self):
        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            self.draw_widget_rect(self.root, canvas)
            self.root.draw()

        super()._draw()

    def draw_widget_rect(self, widget: Widget, canvas: skia.Canvas, depth=0, max_depth=6):
        # global_position accumulates parent offsets; yoga's computed
        # left/top are parent-relative.
        position = widget.global_position
        size = widget.size

        # Darker at depth 0, lighter as depth increases.
        depth = min(depth, max_depth)
        shade = int(32 + (224 * depth // max_depth))  # 32 to 255
        color = (0xFF << 24) | (shade << 16) | (shade << 8) | shade  # ARGB

        paint = skia.Paint()
        paint.set_color(color)
        # The binding's Rect is XYWH, not SkRect's LTRB.
        rect = skia.Rect(position.x, position.y, size.x, size.y)
        canvas.draw_rect(rect, paint)

        '''
        canvas.draw_string(
            f"Node {depth}", position.x + 5, position.y + 15, self.font, self.text_paint
        )
        '''

        for child in widget.children:
            self.draw_widget_rect(child, canvas, depth=depth + 1, max_depth=max_depth)


def install(app: App):
    app.add_channel(PageChannel(FlexRowPage, "flex_row", "Flex Row"))