from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import glm
    from ...model import Model
    from ...widget import Widget
    from .. import Scene

from ... import Node

from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED

class SceneLayer(Node["SceneLayer"]):
    is_scene = False

    def __init__(self, name: str, model: "Model" = None) -> None:
        super().__init__(model=model)
        self.name = name
        # self.scene: Scene = None
        self.layers_by_name: dict[str, SceneLayer] = {}

    @property
    def scene(self) -> "Scene":
        node = self
        while node is not None:
            if node.is_scene:
                return node
            node = node.parent
        return None

    def add_layer(self, layer: "SceneLayer"):
        # layer.scene = self
        self.add_child(layer)
        self.layers_by_name[layer.name] = layer
        return layer

    def remove_layer(self, layer: "SceneLayer"):
        self.remove_child(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)

    def widget_at(self, point: "glm.vec2") -> "tuple[Widget, glm.vec2] | None":
        """Topmost embedded widget tree under a world point.

        Same order as dispatch_2d, so hover and clicks always agree on
        which control is on top.
        """
        for child in reversed(self.children):
            hit = child.widget_at(point)
            if hit is not None:
                return hit
        return None

    def dispatch(self, event) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch(event):
                return EVENT_HANDLED
        return super().dispatch(event)
