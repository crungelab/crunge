from loguru import logger
import glm

from crunge import skia

from ..renderer import Renderer
from ..view_layer import ViewLayer

from .. import colors
from ..color import rgba_tuple_to_argb_int

class ScratchLayer(ViewLayer):
    def __init__(self):
        super().__init__("ScratchLayer", priority=900)
        self.draw_calls = []

    def add_call(self, call):
        self.draw_calls.append(call)
        
    def draw_line(self, begin: glm.vec2, end: glm.vec2, color=colors.WHITE):
        #logger.debug(f"DemoView.draw_line({begin}, {end}, {color})")
        def draw(renderer: Renderer, canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(color))
            canvas.draw_line(begin[0], begin[1], end[0], end[1], paint)

        self.add_call(draw)

    def draw_polygon(self, points: list[glm.vec2], outline_color=colors.WHITE):
        def draw(renderer: Renderer, canvas: skia.Canvas):
            path = skia.Path()
            if not points:
                return
            path.move_to(*points[0])
            for pt in points[1:]:
                path.line_to(*pt)
            path.close()

            outline_paint = skia.Paint()
            outline_paint.set_color(rgba_tuple_to_argb_int(outline_color))
            outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            outline_paint.set_stroke_width(1.0)

            canvas.draw_path(path, outline_paint)
        
        self.add_call(draw)

    def draw_circle(self, center: glm.vec2, radius: float, segments: int = 32, color=colors.WHITE):
        def draw(renderer: Renderer, canvas: skia.Canvas):
            #logger.debug(f"draw_circle({center}, {radius}, {segments}, {color})")
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(color))
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(2)  # Set the outline thickness as needed
            canvas.draw_circle(skia.Point(center.x, center.y), radius, paint)

        self.add_call(draw)

    def post_draw(self, renderer: Renderer):
        with renderer.canvas_target() as canvas:
            canvas.save()

            canvas.translate(renderer.viewport.width // 2, renderer.viewport.height // 2)
            scale = 1 / renderer.camera_2d.zoom
            canvas.scale(scale, -scale)  # Invert Y-axis for Skia
            camera_x, camera_y = renderer.camera_2d.position.x, renderer.camera_2d.position.y
            canvas.translate(-camera_x, -camera_y)     # pan to camera

            for call in self.draw_calls:
                call(renderer, canvas)

            canvas.restore()

        self.draw_calls.clear()
        super().post_draw(renderer)


