import glm

from ..renderer import Renderer
from ..view_layer import ViewLayer

from .vu_2d import Vu2D
from .shape.line_2d import Line2D
from .shape.polygon_2d import Polygon2D
from .shape.circle_2d import Circle2D

from .. import colors

class ScratchLayer(ViewLayer):
    def __init__(self):
        super().__init__("ScratchLayer")
        self.vu_list: list[Vu2D] = []

    def add_vu(self, vu: Vu2D):
        vu.enable()
        self.vu_list.append(vu)
    
    def remove_vu(self, vu: Vu2D):
        self.vu_list.remove(vu)
    
    def draw_line(self, begin: glm.vec2, end: glm.vec2, color=colors.WHITE):
        line = Line2D(begin, end, color)
        self.add_vu(line)

    def draw_polygon(self, points: list[glm.vec2], color=colors.WHITE):
        polygon = Polygon2D(points, color)
        self.add_vu(polygon)
    
    def draw_circle(self, center: glm.vec2, radius: float, segments: int = 32, color=colors.WHITE):
        circle = Circle2D(center, radius, segments, color)
        self.add_vu(circle)

    def draw(self, renderer: Renderer):
        # logger.debug("DemoView.draw()")
        for vu in self.vu_list:
            vu.draw(renderer)
        self.vu_list.clear()
        super().draw(renderer)
