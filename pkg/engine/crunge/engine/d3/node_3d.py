# node_3d.py
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .scene.scene_3d import Scene3D
    from .vu_3d import Vu3D

from loguru import logger
import glm

from ..math import Bounds3
from ..scene.scene_node import SceneNode


class Node3D(SceneNode["Node3D", "Scene3D"]):
    def __init__(
        self, position=glm.vec3(), vu: "Vu3D" = None, model: Any = None
    ) -> None:
        super().__init__(vu, model)
        self._position = position
        self._orientation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self._scale = glm.vec3(1.0)

        # Local transform: rebuilt from position/orientation/scale.
        self._local_transform = glm.mat4(1.0)

        # Global (world) transform: local transform chained through ancestors.
        self._global_transform = glm.mat4(1.0)

        # NOTE: local bounds mapped into world space only - does NOT merge
        # child bounds the way the old update_bounds() did. See chat note.
        self._bounds = Bounds3()

    def on_transform(self):
        self.gpu_update_model()

    # TODO: DEPRECATED: this should be handled by the Vu class
    def gpu_update_model(self):
        pass

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def position(self) -> glm.vec3:
        return self._position

    @position.setter
    def position(self, value: glm.vec3):
        if value == self._position:
            return
        self._position = value
        self._mark_local_dirty()
        self.on_position()

    def on_position(self):
        pass

    @property
    def orientation(self) -> glm.quat:
        return self._orientation

    @orientation.setter
    def orientation(self, value: glm.quat):
        if value == self._orientation:
            return
        self._orientation = value
        self._mark_local_dirty()

    @property
    def scale(self) -> glm.vec3:
        return self._scale

    @scale.setter
    def scale(self, value: glm.vec3):
        if value == self._scale:
            return
        self._scale = value
        self._mark_local_dirty()

    # ------------------------------------------------------------------
    # Local transform (was `matrix`)
    # ------------------------------------------------------------------

    @property
    def transform(self) -> glm.mat4:
        """Local transform (position/orientation/scale only, no ancestors)."""
        if self._local_dirty:
            self._update_local_transform()
        return self._local_transform

    """
    @transform.setter
    def transform(self, value: glm.mat4):
        self._local_transform = value
        self._local_dirty = False
        self._mark_global_dirty()
    """
    @transform.setter
    def transform(self, value: glm.mat4):
        self._position = glm.vec3(value[3])
        m = glm.mat3(value)
        scale = glm.vec3(glm.length(m[0]), glm.length(m[1]), glm.length(m[2]))
        self._scale = scale
        # Normalize out scale before extracting rotation - quat_cast needs
        # an orthonormal basis (same issue as global_orientation).
        if scale.x != 0: m[0] /= scale.x
        if scale.y != 0: m[1] /= scale.y
        if scale.z != 0: m[2] /= scale.z
        self._orientation = glm.quat_cast(m)
        self._local_transform = value
        self._local_dirty = False
        self._mark_global_dirty()

    def _update_local_transform(self):
        matrix = glm.mat4(1.0)
        matrix = glm.translate(matrix, self._position)
        matrix = matrix * glm.mat4_cast(self._orientation)
        matrix = glm.scale(matrix, self._scale)
        self._local_transform = matrix
        self._local_dirty = False

    # ------------------------------------------------------------------
    # Global (world) transform (was `transform`)
    # ------------------------------------------------------------------

    @property
    def global_transform(self) -> glm.mat4:
        if self._global_dirty:
            self._update_global_transform()
        return self._global_transform

    def _update_global_transform(self):
        if self.parent is not None:
            self._global_transform = self.parent.global_transform * self.transform
        else:
            self._global_transform = self.transform
        self._global_dirty = False

    # ------------------------------------------------------------------
    # Global decomposed properties (new, Godot-style)
    # ------------------------------------------------------------------

    @property
    def global_position(self) -> glm.vec3:
        m = self.global_transform
        return glm.vec3(m[3].x, m[3].y, m[3].z)

    @global_position.setter
    def global_position(self, value: glm.vec3):
        if self.parent is not None:
            parent_inv = glm.inverse(self.parent.global_transform)
            local = parent_inv * glm.vec4(value.x, value.y, value.z, 1.0)
            self.position = glm.vec3(local.x, local.y, local.z)
        else:
            self.position = value

    @property
    def global_orientation(self) -> glm.quat:
        m = glm.mat3(self.global_transform)
        m[0] = glm.normalize(m[0])
        m[1] = glm.normalize(m[1])
        m[2] = glm.normalize(m[2])
        return glm.quat_cast(m)

    """
    @property
    def global_orientation(self) -> glm.quat:
        m = self.global_transform
        return glm.quat_cast(glm.mat3(m))
    """

    @global_orientation.setter
    def global_orientation(self, value: glm.quat):
        if self.parent is not None:
            self.orientation = glm.inverse(self.parent.global_orientation) * value
        else:
            self.orientation = value

    @property
    def global_scale(self) -> glm.vec3:
        m = self.global_transform
        return glm.vec3(
            glm.length(glm.vec3(m[0])),
            glm.length(glm.vec3(m[1])),
            glm.length(glm.vec3(m[2])),
        )

    @global_scale.setter
    def global_scale(self, value: glm.vec3):
        if self.parent is not None:
            p = self.parent.global_scale
            self.scale = glm.vec3(value.x / p.x, value.y / p.y, value.z / p.z)
        else:
            self.scale = value

    # ------------------------------------------------------------------
    # Bounds
    # ------------------------------------------------------------------

    @property
    def bounds(self) -> Bounds3:
        if self._bounds_dirty:
            self._update_bounds()
        return self._bounds

    def _update_bounds(self):
        if self.model is not None:
            self._bounds = self.model.bounds.to_global(self.global_transform)
        else:
            self._bounds = Bounds3()
        self._bounds_dirty = False

    def get_subtree_bounds(self) -> Bounds3:
        """Union of this node's own bounds with every descendant's bounds,
        computed fresh on each call by walking the subtree. NOT cached/dirty-
        tracked like `.bounds` - this is for occasional use (framing a camera,
        computing scene extents), not per-frame queries. Nodes without a model
        contribute nothing but still recurse into their children."""
        bounds = Bounds3()
        if self.model is not None:
            bounds.merge(self.bounds)
        for child in self.children:
            child_bounds = child.get_subtree_bounds()
            if child_bounds.is_valid():
                bounds.merge(child_bounds)
        return bounds

    def get_max_extent(self) -> float:
        """Convenience: largest dimension of this subtree's combined bounds."""
        size = self.get_subtree_bounds().size
        return max(size.x, size.y, size.z)
