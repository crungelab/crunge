from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar

from .base import Base  # ASSUMPTION: Base provides the Lifetime machinery

if TYPE_CHECKING:
    from .base_node import BaseNode

N = TypeVar("N", bound="BaseNode")


class Chip(Base, Generic[N]):
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

    The vu is a chip like any other and takes its place in that walk; there
    is no separate slot for it.
    """

    # Set automatically from whether the subclass overrides the broadcast.
    # Declaring one explicitly in the class body wins — do that when the
    # chip draws or dispatches through a helper rather than an override.
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
        """Resolve sibling chips and cache them. Register listeners.

        e.g.  self.mod = self.node.require(Mod)
              self.node.transform_changed.connect(self.on_transform_changed)
        """

    def unplug(self) -> None:
        """Drop cached sibling references and deregister listeners.

        Runs while the rest of the chip set is still intact, so it is safe
        to touch siblings here.
        """

    def on_detached(self) -> None:
        self._node = None

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