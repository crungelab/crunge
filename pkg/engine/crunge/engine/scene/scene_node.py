from typing import TYPE_CHECKING, ClassVar, TypeVar, Generic

from loguru import logger

from ..node import Node, T_Node
from .layer.scene_layer import SceneLayer

T_Layer = TypeVar("T_Layer", bound=SceneLayer)


class SceneNode(Node[T_Node], Generic[T_Node, T_Layer]):
    children: "list[SceneNode[T_Node, T_Layer]]"

    # When True this node's local transform IS its world transform: subclasses
    # skip the parent chain when composing global, and the dirt cascade below
    # stops here. The node's own children still parent to it normally.
    top_level_default: ClassVar[bool] = False

    def __init__(self, model=None) -> None:
        super().__init__(model)
        self.layer: T_Layer = None

        self._local_dirty = False
        self._global_dirty = False
        self._bounds_dirty = False

        self._transform_notify_pending = False
        self._transform_notify_again = False

        self._top_level = self.top_level_default

    @property
    def top_level(self) -> bool:
        return self._top_level

    @top_level.setter
    def top_level(self, value: bool):
        if value == self._top_level:
            return
        self._top_level = value
        # Local is now read against a different space. Nothing moved in world
        # terms only if the parent chain is identity; otherwise this teleports.
        self._mark_global_dirty()

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

    def _mark_bounds_dirty(self):
        """Invalidate bounds without touching the transform chain.

        Bounds derive from local extents (vu/model size) as well as from the
        global transform. A size change is not a move, so it has no business
        going through _mark_global_dirty — that would emit transform_changed
        and walk the subtree for something that did not move. Call this from
        anything that changes what the node measures: a Vu resolving its
        texture, a model swap, a sprite rect edit.
        """
        self._bounds_dirty = True

    def _mark_global_dirty(self):
        # Flags before the guard. They were set after it, so a transform
        # changed from inside a transform_changed handler set _local_dirty,
        # hit the pending guard, and returned with _global_dirty still
        # False — the move was silently dropped.
        self._global_dirty = True
        self._bounds_dirty = True

        # Re-entry: the flags above are already recorded, but the notify for
        # this new state still has to go out. Setting the flags and returning
        # left handlers holding whatever the previous emit gave them, with no
        # dirty bit anywhere to catch the staleness — signals carry values, so
        # a dropped emit is a dropped value. Ask the active call to loop again.
        if self._transform_notify_pending:
            self._transform_notify_again = True
            return

        self._transform_notify_pending = True
        try:
            while True:
                self._transform_notify_again = False

                for child in self.children:
                    # A top_level child's world transform does not derive from
                    # ours, so our move is a no-op for it and for everything
                    # under it. Don't descend: recursing would recompute an
                    # identical global, re-dirty its bounds, and emit a
                    # transform_changed that says nothing moved — the same
                    # per-frame GPU write cascade top_level exists to avoid.
                    if child.top_level:
                        continue
                    child._mark_global_dirty()

                self.on_transform()
                self.transform_changed.emit(self)

                if not self._transform_notify_again:
                    break
        finally:
            self._transform_notify_pending = False
            self._transform_notify_again = False

    def on_transform(self):
        """Self-notification. Chips use transform_changed; this is for a
        node that needs to react to its own move."""

    def add_child(self, child):
        child.set_layer(self.layer)
        result = super().add_child(child)
        # Reparenting changes a normal child's world transform. A top_level
        # child's is unchanged by definition — but it still has to be marked
        # once here, because it may never have been computed at all.
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