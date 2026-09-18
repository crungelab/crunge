from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from .gfx_access import GfxAccess
from crunge.core.chip import Chip

from .viewport import Viewport
from .easel import Easel
from .renderer import Renderer

if TYPE_CHECKING:
    from .node import Node
    from .vu_group import VuGroup
    from .render_group import RenderGroup


class Vu[T_Node: "Node"](GfxAccess, Chip[T_Node]):
    """The chip that renders its node.

    Subclasses override `_draw`, not `draw`: `draw` owns the boundary work
    that has to happen before anything is emitted, and calls `_draw` to do
    the actual rendering.

    Dirt tracking and enable-scoped listening come from Chip. What Vu adds
    is the specific subscription — transform and model — the draw, and
    membership of a render group.

    A grouped vu does not draw itself. Its per-instance data lives in a
    buffer its VuGroup owns, and the RenderGroup emits it as part of a run.
    `is_grouped` is what a subclass consults before allocating the program,
    buffers and bind groups it would need to draw on its own.
    """
    update_order = 100    # reads transforms

    # Declared rather than inferred. `draw` is overridden here, so the
    # inference in Chip.__init_subclass__ would say True for every Vu
    # regardless; saying it outright keeps the reason visible.
    draws: ClassVar[bool] = True

    # Can this TYPE ever be grouped? A static fact about the vu's geometry,
    # settled before any node or tree exists, which is why it is a class
    # attribute rather than something assigned in __init__. Subclasses
    # override by declaring.
    #
    # False means the geometry is per-instance and cannot be driven from a
    # shared instance buffer — a Spine skeleton with per-frame deformed
    # vertices, say. It does not mean "grouping would be slow here"; that is
    # a registration question, answered by which VuGroup the layer registers.
    groupable: ClassVar[bool] = True

    # `update` is deliberately not overridden. A Vu with nothing to rebuild
    # stays out of the update bucket; one that has something gets there by
    # defining `update` and calling `flush` from it.

    def __init__(self) -> None:
        super().__init__()
        self._group: "VuGroup | None" = None
        self._render_group: "RenderGroup | None" = None

    # -- ambient frame state ----------------------------------------------

    @property
    def current_viewport(self) -> Viewport | None:
        return Viewport.get_current()

    @property
    def current_easel(self) -> Easel | None:
        viewport = self.current_viewport
        return viewport.easel if viewport is not None else None

    @property
    def current_renderer(self) -> Renderer | None:
        return Renderer.get_current()

    # -- listening ---------------------------------------------------------

    def listen(self) -> None:
        node = self.node
        node.transform_changed.connect(self.on_transform_changed)
        node.model_changed.connect(self.on_model_changed)

    def deafen(self) -> None:
        node = self._node
        if node is None:
            return
        node.transform_changed.disconnect(self.on_transform_changed)
        node.model_changed.disconnect(self.on_model_changed)

    def sync(self) -> None:
        """Model first: it is where extents come from, and the transform is
        what gets applied to them. Syncing the transform first applies a
        correct transform to stale extents."""
        node = self.node
        if node.model is not None:
            self.on_model_changed(node)
        self.on_transform_changed(node)

    # -- group -------------------------------------------------------------

    @property
    def group(self) -> "VuGroup | None":
        return self._group

    @group.setter
    def group(self, value: "VuGroup | None") -> None:
        self._group = value
        self.on_group()

    def on_group(self) -> None:
        pass

    @property
    def render_group(self) -> "RenderGroup | None":
        return self._render_group

    @render_group.setter
    def render_group(self, value: "RenderGroup | None") -> None:
        # Settable, because a container that is not a node — deeper's
        # SceneLayer — has to be able to say so itself. The tree walk in
        # _enable cannot reach it.
        self._render_group = value

    @property
    def is_grouped(self) -> bool:
        """Derived, never assigned.

        Keys off the render group rather than the vu group: under
        `is_managed` the append happens later from elsewhere, so `group` is
        still None at enable time and a subclass would wrongly allocate
        resources it will never draw through.
        """
        return self._render_group is not None

    @property
    def sort_key(self):
        """Global draw order. Lower draws first.

        The RenderGroup compares these across every group it owns, so each
        implementation has to return something mutually comparable with the
        rest — keep the shape fixed rather than returning a bare float in
        one place and a tuple in another.
        """
        return 0.0

    def find_render_group(self) -> "RenderGroup | None":
        """Find, but do not choose.

        The vu does not look for a *suitable* vu group. Routing is the
        RenderGroup's job, and splitting that decision in two would mean
        this class had to know what "suitable" means. It also does not
        assign `group`: that comes back through VuGroup.append.
        """
        node = self._node
        if node is not None:
            self._render_group = node.find_render_group()
        return self._render_group

    # -- lifetime ----------------------------------------------------------

    def _enable(self) -> None:
        # Head call: subscribe and sync first, which marks dirt. Anything it
        # writes into waits for the next flush, so membership landing after
        # is safe.
        super()._enable()

        if not self.groupable:
            return

        render_group = self.find_render_group()
        if render_group is not None and not render_group.is_managed:
            render_group.append(self)

    def _disable(self) -> None:
        # Through the render group, not the vu group. VuGroup.remove only
        # drops membership; the plan that actually issues the draw lives one
        # level up, and a run holding this slot keeps drawing it until
        # something invalidates the plan.
        if self._render_group is not None:
            self._render_group.remove(self)
        elif self._group is not None:
            self._group.remove(self)
        self._render_group = None
        super()._disable()

    '''
    def _disable(self) -> None:
        # The load-bearing half. A vu that disables without freeing its slot
        # leaves it occupied, and across a scene reset those accumulate
        # until the buffer fills with members that no longer exist — the
        # same lifetime mismatch that produced the stale entity registry.
        if self._group is not None:
            self._group.remove(self)
        self._render_group = None
        # Tail call: teardown of cross-tree wiring unwinds in the reverse
        # order of _enable's head call.
        super()._disable()
    '''

    # -- signals -----------------------------------------------------------
    #
    # Record and mark. No GPU work here — these fire at arbitrary points in
    # the lifecycle, including before the vu has a buffer.

    def on_transform_changed(self, node: T_Node) -> None:
        pass

    def on_model_changed(self, node: T_Node) -> None:
        pass

    # -- frame -------------------------------------------------------------

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        pass