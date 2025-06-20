from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from loguru import logger

from crunge import yoga

from .. import Renderer
from . import Widget

from ..view_layer import ViewLayer
'''
if TYPE_CHECKING:
    from .scene import Scene
'''

class WidgetLayer(ViewLayer):
    def __init__(self):
        super().__init__("WidgetLayer", priority=950)
        #self.root: Widget = Widget()

    def draw(self, renderer: Renderer) -> None:
        with renderer.canvas_target() as canvas:
            super().draw(renderer)

    '''
    def update(self, dt: float) -> None:
        super().update(dt)
        #self.layout.calculate_bounds(self.width, self.height, yoga.Direction.LTR)
        bounds = self.bounds

        left = bounds.left
        top = bounds.top
        width = bounds.width
        height = bounds.height
        #print(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")
    '''

    '''
    @property
    def nodes(self):
        return self.root.children

    def clear(self):
        self.root.clear()

    def pre_draw(self, renderer: Renderer) -> None:
        self.root.pre_draw(renderer)

    def draw(self, renderer: Renderer) -> None:
        with renderer.canvas_target() as canvas:
            self.root.draw(renderer)

    def post_draw(self, renderer: Renderer) -> None:
        self.root.post_draw(renderer)

    def update(self, dt: float) -> None:
        self.root.update(dt)

    def attach(self, node: Widget) -> None:
        self.root.attach(node)

    def detach(self, node: Widget) -> None:
        self.root.detach(node)
    '''