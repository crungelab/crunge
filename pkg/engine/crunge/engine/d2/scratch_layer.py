import glm

from ..view_layer import ViewLayer
from .vu_2d import Vu2D
from .line_2d import Line2D
from .renderer_2d import Renderer2D

from ..color import Color

class ScratchLayer(ViewLayer):
    def __init__(self):
        super().__init__("ScratchLayer")
        self.vu_list: list[Vu2D] = []

    '''
    def _create(self, view):
        super()._create(view)
        return self
    '''

    def add_vu(self, vu: Vu2D):
        self.vu_list.append(vu)
    
    def remove_vu(self, vu: Vu2D):
        self.vu_list.remove(vu)
    
    #def draw_line(self, begin: glm.vec2, end: glm.vec2, color=glm.vec4(1.0, 1.0, 1.0, 1.0)):
    def draw_line(self, begin: glm.vec2, end: glm.vec2, color=Color.WHITE):
        line = Line2D(begin, end, color)
        self.add_vu(line)
    
    def draw(self, renderer: Renderer2D):
        # logger.debug("DemoView.draw()")
        for vu in self.vu_list:
            vu.draw(renderer)

        super().draw(renderer)

    def post_draw(self, renderer: Renderer2D):
        self.vu_list.clear()
        super().post_draw(renderer)


