from typing import Any

from loguru import logger
import glm

from .node_2d import Node2D


class SizedNode2D(Node2D):
    """A node whose size is set rather than derived from its model.

    Node2D takes its local_size from the model, which is right when the model
    is a fixed piece of art. A nine patch is the other way round: the model
    supplies the borders and the node decides how big the thing is. This is
    also where a layout engine writes its result.
    """

    def __init__(
        self,
        position: glm.vec2 = None,
        rotation=0.0,
        scale: glm.vec2 = None,
        model: Any = None,
        size: glm.vec2 = None,
        children: list[Node2D] = None,
    ) -> None:
        self._size: glm.vec2 = glm.vec2(size) if size is not None else None
        super().__init__(position, rotation, scale, model, children)

    @property
    def local_size(self) -> glm.vec2:
        if self._size is not None:
            return self._size
        return super().local_size

    @local_size.setter
    def local_size(self, value: glm.vec2) -> None:
        value = glm.vec2(value)
        if self._size is not None and value == self._size:
            return
        self._size = value
        self.on_size_changed()

    @property
    def size(self) -> glm.vec2:
        return self.local_size * self.scale

    @size.setter
    def size(self, value: glm.vec2) -> None:
        """Sets the size the node draws at, before its scale."""
        self.local_size = value

    @property
    def local_collision_size(self) -> glm.vec2:
        # Collision follows what is drawn, not the source art
        if self._size is not None:
            return self._size
        return super().local_collision_size

    def on_size_changed(self) -> None:
        self._mark_bounds_dirty()
        # ASSUMPTION: no size-changed signal on SceneNode. The vu rebuilds its
        # transform and bounds from vu.size, which reads local_size, and marks
        # GPU dirt. Replace with the engine's own notification if one lands.
        if self.vu is not None:
            self.vu.on_transform_changed(self)
