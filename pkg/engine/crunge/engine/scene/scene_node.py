from typing import TYPE_CHECKING, TypeVar, Generic

from loguru import logger

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
        return self.layer.scene if self.layer is not None else None

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
        # Flags before the guard. They were set after it, so a transform
        # changed from inside a transform_changed handler set _local_dirty,
        # hit the pending guard, and returned with _global_dirty still
        # False — the move was silently dropped.
        self._global_dirty = True
        self._bounds_dirty = True

        if self._transform_notify_pending:
            return
        self._transform_notify_pending = True

        for child in self.children:
            child._mark_global_dirty()

        try:
            self.on_transform()
            self.transform_changed.emit(self)
        finally:
            self._transform_notify_pending = False

    def on_transform(self):
        """Self-notification. Chips use transform_changed; this is for a
        node that needs to react to its own move."""

    def add_child(self, child):
        child.set_layer(self.layer)
        result = super().add_child(child)
        child._mark_global_dirty()
        return result

    def remove_child(self, child):
        result = super().remove_child(child)
        # After: super().remove_child disables the child, and anything
        # reading `scene` on the way down needs the layer still attached.
        child.set_layer(None)
        child._mark_global_dirty()
        return result

    def set_layer(self, layer: T_Layer) -> None:
        """Assigning `layer` directly left an already-populated subtree with
        its descendants pointing at nothing."""
        self.layer = layer
        for child in self.children:
            child.set_layer(layer)