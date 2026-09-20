from __future__ import annotations

from typing import Any

from loguru import logger
import glm

from crunge import yoga

from ..math import Bounds2
from ..layout import Layout

from .settings_2d import Settings2D

from .node_2d import Node2D


class Layout2D(Layout["Control2D"]):
    """Scene-space layout.

    Same yoga engine as WidgetLayout, different landing zone. Widget keeps
    yoga's convention verbatim -- y-down, integer pixels -- because widget
    space *is* that convention. A Control2D lands in the scene instead, where
    y is up, coordinates are floats, and a node's rect is centered on its
    position rather than hanging off its top-left corner. Control2D.on_layout
    reconciles all three, and it is the only place any of them is reconciled.

    Styles are authored in world units, which is why the config below exists:
    yoga rounds computed edges to whole points, and a point has to be a pixel
    rather than a metre or the whole UI quantizes to the metre.
    """

    _config: yoga.Config = None

    @classmethod
    def get_config(cls) -> yoga.Config:
        # Lazy, so importing this module does not require yoga to be ready.
        # One config for every Layout2D ever made, held for the process
        # lifetime: Config.create hands back a non-owning reference, so this
        # class attribute is what keeps it alive behind every node using it.
        if cls._config is None:
            config = yoga.Config.create()
            config.set_point_scale_factor(Settings2D().ppu)
            cls._config = config
        return cls._config

    @property
    def measurable(self) -> bool:
        return True


class Control2D(Node2D):
    """A Node2D whose rect is computed by yoga, laid out like a Widget.

    Geometry flows one way: style -> yoga -> on_layout -> position/size. The
    control owns its size from the first layout pass on, which is just
    Node2D's `_size` sentinel doing its job -- no sized-node subclass, and no
    per-node origin field. Yoga's corner convention lives entirely inside
    on_layout, run once per pass, instead of in a field every vu would have to
    consult on every transform rebuild.
    """

    def __init__(
        self,
        position: glm.vec2 = None,
        rotation=0.0,
        scale: glm.vec2 = None,
        model: Any = None,
        children: list["Control2D"] = None,
        size: glm.vec2 = None,
        style: yoga.Style = None,
    ) -> None:
        # style last, so Node2D's positional order is unchanged for existing
        # call sites. Everything here reads better as keywords anyway.
        super().__init__(position, rotation, scale, model, children, size)

        self.layout = Layout2D(style)
        self.add_chip(self.layout)  # ASSUMPTION: node-side chip attachment

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def on_layout(self, layout: Layout) -> None:
        """Land a yoga result in the scene.

        Three conversions, all of them here and nowhere else:

        * y-down to y-up, so `top` counts downwards from the parent's top edge
        * corner to center, because a Node2D's rect is centered on its position
        * parent corner to parent center, because the parent's rect is centered
          on *its* position too, putting its top-left at (-pw/2, +ph/2) in
          parent-local coordinates

        That last one is why `layout.parent_size` exists. Dropping it and
        treating the parent's position as its top-left is only correct when the
        parent happens to be the layout root.
        """
        size = glm.vec2(layout.width, layout.height)
        changed = self._size is None or size != self._size

        if layout.is_root:
            # parent_size reports our own size at the root, which would work
            # out to (0, 0) and teleport a control that was placed in the
            # world. A root takes its size from yoga and keeps its position.
            pass
        else:
            parent = layout.parent_size
            # Position before size: the unscaled_size setter fires
            # on_size_changed, which pushes a rebuilt transform at the vu.
            # The other order hands the vu a new size against a stale
            # position for one frame.
            self.position = glm.vec2(
                -parent.x * 0.5 + layout.left + size.x * 0.5,
                parent.y * 0.5 - layout.top - size.y * 0.5,
            )

        self.unscaled_size = size

        if changed:
            self.on_size()

    def on_size(self) -> None:
        """Fires when the computed size changes. Same name and contract as
        Widget.on_size."""

    def on_measure(
        self, width: float, width_mode: str, height: float, height_mode: str
    ) -> glm.vec2:
        """Intrinsic size, for yoga to use when the style does not give one.

        This is what makes a control behave like an <img>: give it no style
        size and it comes out at its model's natural size; constrain it and it
        fits the constraint. Without it, every call site has to tell yoga a
        size the control already knew.

        Measures against intrinsic_size, never unscaled_size. Once a layout
        pass has run, unscaled_size holds that pass's result, so measuring
        against it would feed each pass its own previous answer -- the model
        is the thing with an opinion that does not move.

        Called repeatedly while flex resolves, so it reads and returns and
        does nothing else. Writing a size from here, or marking anything
        dirty, is a loop that never settles.

        Squeezing drops the excess on the constrained axis rather than
        scaling both. A sprite that should shrink proportionally wants yoga's
        aspect_ratio style, which costs nothing per pass; doing it here
        instead makes the ratio invisible to the flex algorithm.
        """
        natural = self.intrinsic_size
        return glm.vec2(
            self._measure_axis(natural.x, width, width_mode),
            self._measure_axis(natural.y, height, height_mode),
        )

    @staticmethod
    def _measure_axis(natural: float, available: float, mode: str) -> float:
        if mode == "exactly":
            return available
        if mode == "at_most":
            return min(natural, available)
        return natural

    @property
    def style(self) -> yoga.Style:
        return self.layout.style

    @style.setter
    def style(self, value: yoga.Style) -> None:
        self.layout.style = value

    # ------------------------------------------------------------------
    # Corner handles
    #
    # Derived, not stored: position stays the single source of truth, so
    # nothing can drift out of agreement with it. All in the parent's space,
    # which is centered on the parent's position -- these are not yoga
    # coordinates and do not compose with layout.left / layout.top.
    # ------------------------------------------------------------------

    @property
    def top_left(self) -> glm.vec2:
        half = self.size * 0.5
        return glm.vec2(self._position.x - half.x, self._position.y + half.y)

    @top_left.setter
    def top_left(self, value: glm.vec2) -> None:
        half = self.size * 0.5
        self.position = glm.vec2(value.x + half.x, value.y - half.y)

    def get_parent_rect(self) -> Bounds2:
        """This control's rect in its parent's space, scale included.

        Rotation is ignored, which is the right answer for laying out siblings
        and the wrong one for a rotated control. Use global_bounds for that.
        """
        half = self.size * 0.5
        p = self._position
        return Bounds2(p.x - half.x, p.y - half.y, p.x + half.x, p.y + half.y)

    def set_rect(self, top_left: glm.vec2, size: glm.vec2) -> None:
        """Place by corner and size together, for a control yoga does not own.

        Prefer this to writing unscaled_size alone: position is the middle of
        the rect, so a lone size change grows the control both ways and walks
        its corner by half the delta. Widget dodges this by making its setters
        raise and letting only on_layout write; a laid-out Control2D is in the
        same position, but one placed by hand is not, so the sharp edge stays.
        """
        self.unscaled_size = glm.vec2(size)
        self.top_left = glm.vec2(top_left)

    # ------------------------------------------------------------------
    # Hit testing
    # ------------------------------------------------------------------

    def hit_test(self, x: float, y: float) -> bool:
        """Is this world-space point inside the control's rect?

        Widget compares against a summed integer offset because widget space
        has no rotation or scale. A control is a scene node, so this goes
        through the inverse global transform and a rotated control tests
        against its actual rect rather than its AABB. One mat4 inverse per
        call, which is nothing at UI cardinalities and would matter if it ran
        per entity per frame.
        """
        inv = glm.inverse(self.global_transform)
        local = inv * glm.vec4(x, y, 0.0, 1.0)
        # local.z comes back as -depth and is deliberately ignored: this is a
        # 2D rect test, the depth only ever ordered the draw.
        half = self.unscaled_size * 0.5
        return -half.x <= local.x <= half.x and -half.y <= local.y <= half.y