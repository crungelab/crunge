from __future__ import annotations

from enum import IntFlag, auto
from typing import TYPE_CHECKING, Any, ClassVar

from .base import Base

if TYPE_CHECKING:
    from .base_node import BaseNode


class Dirt(IntFlag):
    """What a chip owes the next flush.

    One member per thing that gets rebuilt independently. Transform is not
    a member: the node owns the transform and already tracks its own dirty
    state, so a second flag here would be a duplicate source of truth.
    """

    NONE = 0
    GEOMETRY = auto()  # vertex/index data the chip owns
    BINDING = auto()  # bind groups, which reference the buffers below
    GPU = auto()  # uniform data the chip owns


class Chip[N: "BaseNode"](Base):
    """A unit of behaviour owned by a node.

    Lifetime is driven entirely by the owner. A chip never creates or
    destroys itself; `BaseNode` walks its chip set inside `create_children`,
    `enable_children`, `_disable` and `destroy_children`, so a chip added to
    an already-created node is brought up to date on `add()`.

    Ordering within a node, for the record:

        create     chips -> children
        enable     chips -> children
        update     chips -> children
        draw       chips -> children
        disable    children -> chips
        destroy    children -> chips

    Two patterns live here because more than the vu needs them:

    Listening is scoped to enablement. A disabled chip is not subscribed at
    all, so nothing it owns can be touched while it is not participating,
    and there is no per-emit `if self.enabled` branch on a hot path.
    `_enable` calls `sync`, which catches up on everything that changed
    while it was disconnected.

    Handlers record state and mark dirt; they never touch the GPU. Rebuilds
    happen in `flush`, which a chip with GPU state calls from `update` —
    before the render pass opens, since buffer writes are illegal once it
    has. Each domain clears only on success, so a rebuild that runs before
    its target exists is retried without dragging the others along.
    """

    # Set automatically from whether the subclass overrides the broadcast.
    # Declaring one explicitly in the class body wins — do that when the
    # chip draws or dispatches through a helper rather than an override.
    update_order = 0

    updates: ClassVar[bool] = False
    draws: ClassVar[bool] = False
    dispatches: ClassVar[bool] = False

    _BROADCASTS: ClassVar[tuple[tuple[str, str], ...]] = (
        ("updates", "update"),
        ("draws", "draw"),
        ("dispatches", "dispatch"),
    )

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for flag, method in Chip._BROADCASTS:
            if flag in cls.__dict__:
                continue  # explicit declaration, leave it alone
            setattr(cls, flag, getattr(cls, method) is not getattr(Chip, method))

    def __init__(self) -> None:
        super().__init__()
        self._node: N | None = None
        self._dirt = Dirt.NONE

    # -- ownership ---------------------------------------------------------

    @property
    def node(self) -> N:
        node = self._node
        if node is None:
            raise RuntimeError(f"{type(self).__name__} is not attached to a node")
        return node

    @property
    def attached(self) -> bool:
        return self._node is not None

    # -- attach lifecycle --------------------------------------------------
    #
    # Two phases. `on_attached` fires the moment the chip is seated, when
    # the board around it is unfinished and siblings may not exist yet.
    # `plug` fires from `create_children`, once the chip set is complete
    # and every chip has been created, and is the only safe place to
    # resolve siblings. Resolve there, cache the reference, never look up
    # per frame.

    def on_attached(self, node: N) -> None:
        self._node = node

    def plug(self) -> None:
        """Resolve sibling chips and cache them.

        e.g.  self.mod = self.node.require(Mod)
        """

    def unplug(self) -> None:
        """Drop cached sibling references.

        Runs while the rest of the chip set is still intact, so it is safe
        to touch siblings here.
        """

    def on_detached(self) -> None:
        self.deafen()
        self._node = None

    # -- listening ---------------------------------------------------------

    def _enable(self) -> None:
        super()._enable()
        if not self.attached:
            return  # standalone chip: no node state to track
        self.listen()
        self.sync()

    def _disable(self) -> None:
        self.deafen()
        super()._disable()

    def listen(self) -> None:
        """Subscribe to node state. Signal.connect dedupes, so an
        implementation needs no flag of its own."""

    def deafen(self) -> None:
        """Unsubscribe. Must tolerate never having listened, and must read
        `self._node` rather than `self.node` — it runs during detach."""

    def sync(self) -> None:
        """Catch up on state that changed while unsubscribed."""

    # -- dirt --------------------------------------------------------------

    @property
    def dirt(self) -> Dirt:
        return self._dirt

    @property
    def dirty(self) -> bool:
        return self._dirt is not Dirt.NONE

    def mark(self, dirt: Dirt) -> None:
        self._dirt |= dirt

    def mark_geometry(self) -> None:
        self.mark(Dirt.GEOMETRY)

    def mark_binding(self) -> None:
        self.mark(Dirt.BINDING)

    def mark_gpu(self) -> None:
        self.mark(Dirt.GPU)

    def flush(self) -> None:
        """Rebuild whatever is owed. Safe every frame; cheap when clean.

        Explicit per-domain dispatch rather than a table: the order between
        domains is load-bearing, and a rebuild that feeds another has to
        run first. Geometry before binding, since vertex data can change
        what a bind group describes; binding before the uniform write,
        since a bind group has to exist before anything reads through it.
        """
        dirt = self._dirt
        if dirt is Dirt.NONE:
            return

        if dirt & Dirt.GEOMETRY and self._flush_geometry():
            self._dirt &= ~Dirt.GEOMETRY

        if dirt & Dirt.BINDING and self._flush_binding():
            self._dirt &= ~Dirt.BINDING

        if dirt & Dirt.GPU and self._flush_gpu():
            self._dirt &= ~Dirt.GPU

    def _flush_geometry(self) -> bool:
        """Rebuild vertex/index data. Return False if the target is not
        there yet — the flag stays set and retries on the next flush."""
        return True

    def _flush_binding(self) -> bool:
        """Rebuild bind groups. Return False if a resource they reference
        does not exist yet — the flag stays set and retries."""
        return True

    def _flush_gpu(self) -> bool:
        """Write uniform data. Return False if the target is not there yet
        — the flag stays set and retries on the next flush."""
        return True

    # -- broadcasts --------------------------------------------------------
    #
    # `draw` takes no target. The frame and its API boundary come from the
    # ambient context, same as everywhere else.

    def update(self, delta_time: float) -> None: ...

    def draw(self) -> None: ...

    def dispatch(self, event: Any) -> bool:
        """Return True to consume the event and stop propagation."""
        return False

    def __repr__(self) -> str:
        owner = type(self._node).__name__ if self._node else "detached"
        return f"<{type(self).__name__} on {owner}>"