from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

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
        #self.root: Widget = None
        self.root: Widget = Widget()

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