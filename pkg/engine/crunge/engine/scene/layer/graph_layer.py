from typing import TYPE_CHECKING

from loguru import logger

from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED

from ..scene_node import SceneNode

if TYPE_CHECKING:
    import glm
    from ...widget import Widget
    from .. import Scene

from .scene_layer import SceneLayer

class GraphLayer[T_Node: SceneNode](SceneLayer):
    scene: "Scene[T_Node]"

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.root: SceneNode[T_Node] = None
        self._controls: list[T_Node] = []

    def __iter__(self):
        """Make GraphLayer iterable by returning iterator over nodes"""
        return iter(self.nodes)

    def __len__(self):
        """Return the number of nodes in the GraphLayer"""
        return len(self.nodes)

    @property
    def nodes(self) -> list[T_Node]:
        return self.root.children

    def add_control(self, dispatcher: T_Node):
        self._controls.append(dispatcher)

    def remove_control(self, dispatcher: T_Node):
        self._controls.remove(dispatcher)

    def _create(self) -> None:
        super()._create()
        self.root.create()

    def _enable(self) -> None:
        super()._enable()
        self.root.enable()

    def _disable(self) -> None:
        super()._disable()
        self.root.disable()

    def _destroy(self) -> None:
        super()._destroy()
        self.root.destroy()

    def _ready(self) -> None:
        super()._ready()
        self.root.ready()

    def clear(self) -> None:
        self.root.clear()

    def _draw(self) -> None:
        self.root.draw()

    def update(self, dt: float) -> None:
        self.root.update(dt)

    def attach(self, node: T_Node) -> None:
        self.root.add_child(node)

    def detach(self, node: T_Node) -> None:
        self.root.remove_child(node)

    def widget_at(self, point: "glm.vec2") -> "tuple[Widget, glm.vec2] | None":
        """Controls first, then child layers -- the dispatch_2d order.

        Only enabled controls are in _controls, so a disabled control drops
        out of hover on the next refresh without anything else to do.
        """
        for control in reversed(self._controls):
            hit = control.widget_at(point)
            if hit is not None:
                return hit
        return super().widget_at(point)

    def dispatch(self, input) -> DispatchResult:
        for control in reversed(self._controls):
            logger.debug(f"Dispatching input {input} to control {control}")
            if control.dispatch(input):
                return EVENT_HANDLED
        return super().dispatch(input)
