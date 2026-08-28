from typing import TYPE_CHECKING, TypeVar, Generic

from loguru import logger

from crunge.engine import Vu

from ..node import Node, T_Node
from .layer.scene_layer import SceneLayer

T_Layer = TypeVar("T_Layer", bound=SceneLayer)


class SceneNode(Node[T_Node], Generic[T_Node, T_Layer]):
    children: "list[SceneNode[T_Node, T_Layer]]"

    def __init__(self, model=None) -> None:
        super().__init__(model)
        self.layer: T_Layer = None

        self._local_dirty = False
        self._global_dirty = False
        self._bounds_dirty = False

        self._transform_notify_pending = False

    @property
    def scene(self):
        return self.layer.scene

    def _create(self):
        super()._create()
        self._mark_local_dirty()

    # ------------------------------------------------------------------
    # Dirty propagation
    # ------------------------------------------------------------------

    def _mark_local_dirty(self):
        self._local_dirty = True
        self._mark_global_dirty()

    def _mark_global_dirty(self):
        if self._transform_notify_pending:
            return
        self._transform_notify_pending = True
        self._global_dirty = True
        self._bounds_dirty = True

        for child in self.children:
            child._mark_global_dirty()

        try:
            self.on_transform()
            self.transform_changed.emit(self)
        finally:
            self._transform_notify_pending = False

    def on_transform(self):
        pass

    def add_child(self, child):
        child.layer = self.layer
        result = super().add_child(child)
        child._mark_global_dirty()
        return result

    def remove_child(self, child):
        child.layer = None
        result = super().remove_child(child)
        child._mark_global_dirty()
        return result
