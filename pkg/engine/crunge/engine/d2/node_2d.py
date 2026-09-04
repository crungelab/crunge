from typing import TYPE_CHECKING, ClassVar, Type, Dict, List, Any, Callable
import math

if TYPE_CHECKING:
    from .scene.scene_2d import Scene2D
    from .vu_2d import Vu2D

from loguru import logger
import glm

from ..math import Bounds2
from ..scene.scene_node import SceneNode


class Node2D(SceneNode["Node2D", "Scene2D"]):
    vu_class: ClassVar["type[Vu2D] | None"] = None

    def __init__(
        self,
        position: glm.vec2 = None,
        rotation=0.0,
        scale: glm.vec2 = None,
        model: Any = None,
    ) -> None:
        super().__init__(model)
        self._position = position if position is not None else glm.vec2()
        self._depth = 0.0
        self._rotation = rotation  # radians
        self._scale = scale if scale is not None else glm.vec2(1.0, 1.0)

        # Local transform: rebuilt from position/rotation/scale/depth.
        self._local_transform = glm.mat4(1.0)

        # Global (world) transform: local transform chained through ancestors.
        self._global_transform = glm.mat4(1.0)

        # World-space bounds, derived from local bounds + global transform.
        self._bounds = Bounds2()

    def _seat(self) -> None:
        super()._seat()
        if self.vu_class is not None:
            self.add(self.vu_class())
            # The vu is what this node measures. Anything that read `bounds`
            # before now cached the 1x1 fallback from local_size and cleared
            # the dirty flag, and nothing else would ever set it again for a
            # node that does not move.
            self._mark_bounds_dirty()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def position(self):
        # Live reference, not a copy: `node.position.x = 5` mutates in place
        # and skips _mark_local_dirty entirely. Returning a copy would send
        # those writes nowhere instead, which is worse. Grep the call sites
        # before changing this.
        return self._position

    @position.setter
    def position(self, value: glm.vec2):
        self._position = value
        self._mark_local_dirty()

    @property
    def x(self):
        return self._position.x

    @x.setter
    def x(self, value: float):
        if value == self._position.x:
            return
        self._position.x = value
        self._mark_local_dirty()

    @property
    def y(self):
        return self._position.y

    @y.setter
    def y(self, value: float):
        if value == self._position.y:
            return
        self._position.y = value
        self._mark_local_dirty()

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value: float):
        if value == self._depth:
            return
        self._depth = value
        self._mark_local_dirty()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        if value == self._rotation:
            return
        self._rotation = value
        self._mark_local_dirty()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: glm.vec2):
        if value == self._scale:
            return
        self._scale = value
        self._mark_local_dirty()

    @property
    def forward(self) -> glm.vec2:
        world = self.global_transform
        return glm.normalize(glm.vec2(world * glm.vec4(0, 1, 0, 0)))

    # ------------------------------------------------------------------
    # Extents
    #
    # local_* is the node's own measurement, in local space, with no scale
    # applied. That is what feeds get_local_bounds, because the transform
    # applies the scale on the way to world space. Folding scale into the
    # value handed to the transform squares it, and compounds parent scale
    # on top.
    #
    # size / collision_size stay scaled: gameplay code asks how big the thing
    # is, not how big its untransformed source art is.
    # ------------------------------------------------------------------

    @property
    def local_size(self) -> glm.vec2:
        if self.model is not None:
            return glm.vec2(self.model.size.x, self.model.size.y)
        elif self.vu is not None:
            return self.vu.size
        return glm.vec2(1.0)

    @property
    def size(self) -> glm.vec2:
        return self.local_size * self.scale

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    @property
    def radius(self):
        return self.size.x / 2

    @property
    def local_collision_size(self) -> glm.vec2:
        if self.model is not None:
            return glm.vec2(
                self.model.collision_size.x, self.model.collision_size.y
            )
        return self.local_size

    @property
    def collision_size(self) -> glm.vec2:
        return self.local_collision_size * self.scale

    @property
    def collision_width(self):
        return self.collision_size.x

    @property
    def collision_height(self):
        return self.collision_size.y

    @property
    def collision_radius(self):
        return self.collision_size.x / 2

    # ------------------------------------------------------------------
    # Local transform (was `matrix`)
    # ------------------------------------------------------------------

    @property
    def transform(self) -> glm.mat4:
        """Local transform (position/rotation/scale/depth only, no ancestors)."""
        if self._local_dirty:
            self._update_local_transform()
        return self._local_transform

    @transform.setter
    def transform(self, value: glm.mat4):
        # Direct override (e.g. from an external solver). Local is now
        # authoritative/clean, but global + bounds still need rebuilding.
        self._local_transform = value
        self._local_dirty = False
        self._mark_global_dirty()

    def _update_local_transform(self):
        x = self._position.x
        y = self._position.y
        z = self._depth

        matrix = glm.mat4(1.0)
        matrix = glm.translate(matrix, glm.vec3(x, y, z))
        matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self._scale.x, self._scale.y, 1),
        )
        self._local_transform = matrix
        self._local_dirty = False

    # ------------------------------------------------------------------
    # Global (world) transform (was `transform`)
    # ------------------------------------------------------------------

    @property
    def global_transform(self) -> glm.mat4:
        """World transform: this node's local transform chained through ancestors."""
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
    def global_position(self) -> glm.vec2:
        m = self.global_transform
        return glm.vec2(m[3].x, m[3].y)

    @global_position.setter
    def global_position(self, value: glm.vec2):
        if self.parent is not None:
            parent_inv = glm.inverse(self.parent.global_transform)
            local = parent_inv * glm.vec4(value.x, value.y, self._depth, 1.0)
            self.position = glm.vec2(local.x, local.y)
        else:
            self.position = value

    @property
    def global_rotation(self) -> float:
        m = self.global_transform
        return math.atan2(m[0].y, m[0].x)

    @global_rotation.setter
    def global_rotation(self, value: float):
        if self.parent is not None:
            self.rotation = value - self.parent.global_rotation
        else:
            self.rotation = value

    @property
    def global_scale(self) -> glm.vec2:
        m = self.global_transform
        sx = glm.length(glm.vec2(m[0].x, m[0].y))
        sy = glm.length(glm.vec2(m[1].x, m[1].y))
        return glm.vec2(sx, sy)

    @global_scale.setter
    def global_scale(self, value: glm.vec2):
        if self.parent is not None:
            parent_scale = self.parent.global_scale
            self.scale = glm.vec2(value.x / parent_scale.x, value.y / parent_scale.y)
        else:
            self.scale = value

    # ------------------------------------------------------------------
    # Bounds
    # ------------------------------------------------------------------

    @property
    def bounds(self) -> Bounds2:
        if self._bounds_dirty:
            self._update_bounds()
        return self._bounds

    def _update_bounds(self):
        local_bounds = self.get_local_bounds()
        self._bounds = local_bounds.to_global(self.global_transform)
        if not self._bounds.is_valid():
            logger.warning(f"Invalid bounds for {self}: {self._bounds}")
        self._bounds_dirty = False

    def get_local_bounds(self) -> Bounds2:
        half = self.local_size * 0.5
        return Bounds2(-half.x, -half.y, half.x, half.y)

    def intersects(self, other: "Node2D"):
        return self.bounds.intersects(other.bounds)