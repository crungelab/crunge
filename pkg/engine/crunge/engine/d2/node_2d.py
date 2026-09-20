from typing import TYPE_CHECKING, ClassVar, Any
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
        children: list["Node2D"] = None,
        size: glm.vec2 = None,
    ) -> None:
        super().__init__(model, children)
        self._position = position if position is not None else glm.vec2()
        self._depth = 0.0
        self._rotation = rotation  # radians
        self._scale = scale if scale is not None else glm.vec2(1.0, 1.0)

        # None means nothing has written a size, so the node measures to its
        # model. Writing it makes this node the owner of its own size and it
        # stops tracking the model from then on. This is what a nine patch and
        # a layout engine both want: the model supplies the borders, the node
        # decides how big the thing is. See unscaled_size.
        self._size: glm.vec2 | None = glm.vec2(size) if size is not None else None

        # Local transform: rebuilt from position/rotation/scale/depth.
        self._local_transform = glm.mat4(1.0)

        # Global (world) transform: local transform chained through ancestors.
        self._global_transform = glm.mat4(1.0)

        # World-space bounds, derived from local bounds + global transform.
        self._bounds = Bounds2()

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
    # Three values, each answering a different question:
    #
    #   intrinsic_size  what the model says this is, with nothing
    #                   constraining it. Never reflects a written size, so a
    #                   measure function can ask for it without being fed its
    #                   own previous answer.
    #   unscaled_size   what this node is before its transform: the written
    #                   size if there is one, the intrinsic size otherwise.
    #                   This is what feeds get_local_bounds and what the vus
    #                   scale their unit quad by, because the transform
    #                   applies the scale on the way to world space. Folding
    #                   scale in here squares it, and compounds the parent's
    #                   on top.
    #   size            what it draws at: unscaled_size times this node's own
    #                   scale. Gameplay code asks how big a thing is, not how
    #                   big its untransformed source art is.
    #
    # `unscaled_` rather than `local_` on the middle one on purpose. `local_`
    # means "before ancestors" everywhere else in this class -- position,
    # rotation, transform -- and the distinction here is scale, not ancestry.
    # One word doing two jobs ten lines apart is how you end up reaching for a
    # `global_size` that cannot exist: size is a magnitude, not a placement,
    # so there is no space to convert it into. The world footprint of a node
    # is global_bounds.
    # ------------------------------------------------------------------

    @property
    def intrinsic_size(self) -> glm.vec2:
        """The size this node would be with nothing constraining it."""
        if self.model is not None:
            return glm.vec2(self.model.size.x, self.model.size.y)
        if self.vu is not None:
            # Careful: a vu whose own `size` reads back through the node
            # (NinePatchVu does) recurses forever when a node has neither a
            # model nor a written size. Give such nodes a size at construction.
            return self.vu.size
        return glm.vec2(1.0)

    @property
    def unscaled_size(self) -> glm.vec2:
        if self._size is not None:
            # Live reference, same bargain as `position` above: an in-place
            # `node.unscaled_size.x = 5` skips on_size_changed and leaves
            # bounds stale. Handing back a copy would swallow the write.
            return self._size
        return self.intrinsic_size

    @unscaled_size.setter
    def unscaled_size(self, value: glm.vec2) -> None:
        # No equality guard here on purpose. A guard would be comparing against
        # a value whose freshness this setter cannot see, and the first write
        # past None can never short-circuit anyway. If a layout pass writes the
        # same size every frame, guard it at the layout call site, where the
        # input context is known.
        self._size = glm.vec2(value)
        self.on_size_changed()

    @property
    def size(self) -> glm.vec2:
        return self.unscaled_size * self.scale

    @size.setter
    def size(self, value: glm.vec2) -> None:
        """Size after scale, so that a set followed by a get round-trips.

        Use unscaled_size to write the pre-transform measurement directly.
        """
        s = self._scale
        if s.x == 0.0 or s.y == 0.0:
            raise ValueError(
                f"Cannot set size on {self} while scale has a zero component: {s}. "
                "Set unscaled_size instead, or fix the scale first."
            )
        self.unscaled_size = glm.vec2(value.x / s.x, value.y / s.y)

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
    def intrinsic_collision_size(self) -> glm.vec2:
        """The model's own collision box, which may be tighter than its art."""
        if self.model is not None:
            return glm.vec2(
                self.model.collision_size.x, self.model.collision_size.y
            )
        return self.intrinsic_size

    @property
    def unscaled_collision_size(self) -> glm.vec2:
        if self.model is None:
            return self.unscaled_size

        collision = self.intrinsic_collision_size
        if self._size is None:
            return collision

        # A written size keeps the model's collision-to-art ratio rather than
        # snapping the hitbox to the drawn size. A model whose collision box is
        # deliberately tighter than its art keeps that intent at any size, and
        # a model where the two agree still comes out equal to the drawn size.
        art = self.intrinsic_size
        return glm.vec2(
            collision.x * (self._size.x / art.x) if art.x else self._size.x,
            collision.y * (self._size.y / art.y) if art.y else self._size.y,
        )

    @property
    def collision_size(self) -> glm.vec2:
        return self.unscaled_collision_size * self.scale

    @property
    def collision_width(self):
        return self.collision_size.x

    @property
    def collision_height(self):
        return self.collision_size.y

    @property
    def collision_radius(self):
        return self.collision_size.x / 2

    def on_size_changed(self) -> None:
        self._mark_bounds_dirty()
        # ASSUMPTION: no size-changed signal on SceneNode. The vu rebuilds its
        # transform and bounds from the node and marks GPU dirt. Replace with
        # the engine's own notification if one lands.
        if self.vu is not None:
            self.vu.on_transform_changed(self)

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
        """World transform: this node's local transform chained through ancestors.

        For a top_level node there is no chaining: local is world.
        """
        if self._global_dirty:
            self._update_global_transform()
        return self._global_transform

    def _update_global_transform(self):
        if self.top_level or self.parent is None:
            self._global_transform = self.transform
        else:
            self._global_transform = self.parent.global_transform * self.transform
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
        if self.top_level or self.parent is None:
            self.position = value
        else:
            parent_inv = glm.inverse(self.parent.global_transform)
            local = parent_inv * glm.vec4(value.x, value.y, self._depth, 1.0)
            self.position = glm.vec2(local.x, local.y)

    @property
    def global_rotation(self) -> float:
        m = self.global_transform
        return math.atan2(m[0].y, m[0].x)

    @global_rotation.setter
    def global_rotation(self, value: float):
        if self.top_level or self.parent is None:
            self.rotation = value
        else:
            self.rotation = value - self.parent.global_rotation

    @property
    def global_scale(self) -> glm.vec2:
        # Fast path: nothing to chain, so skip decomposing a matrix whose
        # scale we already hold.
        if self.top_level or self.parent is None:
            return self._scale
        m = self.global_transform
        sx = glm.length(glm.vec2(m[0].x, m[0].y))
        sy = glm.length(glm.vec2(m[1].x, m[1].y))
        return glm.vec2(sx, sy)

    @global_scale.setter
    def global_scale(self, value: glm.vec2):
        if self.top_level or self.parent is None:
            self.scale = value
        else:
            parent_scale = self.parent.global_scale
            self.scale = glm.vec2(value.x / parent_scale.x, value.y / parent_scale.y)

    # ------------------------------------------------------------------
    # Bounds
    # ------------------------------------------------------------------

    @property
    def global_bounds(self) -> Bounds2:
        if self._bounds_dirty:
            self._update_bounds()
        return self._bounds

    @property
    def bounds(self):
        raise AttributeError(
            f"{type(self).__name__}.bounds is being repointed from world to local. "
            "Use global_bounds for world-space, get_local_bounds() for local."
        )

    '''
    @property
    def bounds(self) -> Bounds2:
        if self._bounds_dirty:
            self._update_bounds()
        return self._bounds
    '''

    def _update_bounds(self):
        local_bounds = self.get_local_bounds()
        self._bounds = local_bounds.to_global(self.global_transform)
        if not self._bounds.is_valid():
            logger.warning(f"Invalid bounds for {self}: {self._bounds}")
        self._bounds_dirty = False

    def get_local_bounds(self) -> Bounds2:
        half = self.unscaled_size * 0.5
        return Bounds2(-half.x, -half.y, half.x, half.y)

    def intersects(self, other: "Node2D"):
        return self.global_bounds.intersects(other.global_bounds)