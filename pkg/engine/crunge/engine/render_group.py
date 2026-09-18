from typing import Any, Callable, Iterator

from loguru import logger

from crunge.core.chip import Chip

from .renderer import Renderer
from .render_state import RenderState
from .vu import Vu
from .vu_group import VuGroup, Run


class RenderGroup(Chip[Any]):
    """Owns the draw plan for a set of vus of mixed type.

    Routes each vu to a VuGroup by type, orders every member globally, and
    cuts that ordered sequence into runs.

    Two constraints shape everything here:

    A run can never span two groups, because first_instance indexes whatever
    buffer is bound at draw time. So run construction is global but run
    membership is per-group.

    Run construction has to happen during the global walk, not per group
    afterwards. A group computing its own runs in isolation would merge two
    of its members even when a member of another group sorts between them,
    and no amount of sorting the plan afterwards can un-merge them.

    Beyond the sort key, a run is opaque here — the group builds it and the
    group draws it. Nothing in this class assumes a quad, an instance count,
    or even that a run is instanced at all.
    """

    def __init__(self, is_managed: bool = False) -> None:
        super().__init__()
        # is_managed: membership is somebody else's business — a grid that
        # rebuilds an ordered stream explicitly. Vus do not self-append.
        self.is_managed = is_managed

        self.factories: dict[type, Callable[[], VuGroup]] = {}
        self.groups: dict[type, list[VuGroup]] = {}
        self._routes: dict[type, type] = {}

        # Append order, counted here rather than per group. A per-group
        # counter restarts at zero when routing spills into a second group,
        # and the global sort then interleaves that group's first members
        # ahead of the first group's later ones — the draw order silently
        # breaks at exactly the capacity boundary, and only for scenes big
        # enough to reach it.
        self._next_sequence = 0

        self.plan: list[tuple[VuGroup, Run]] = []
        self._replan = False
        self._device_ready = False

    # -- registration ------------------------------------------------------

    def register(self, vu_type: type, factory: Callable[[], VuGroup]) -> None:
        """Register how to build a group for `vu_type`.

        The recipe rather than the instance, because capacity spill means one
        vu type can need several groups and they can't all be built up front.

        The factory is where a model group and a program get in. It closes
        over both; this class never learns what either is, the same way it
        never learns what a run contains.
        """
        self.factories[vu_type] = factory
        self.groups.setdefault(vu_type, [])
        self._routes.clear()

    def route_for(self, vu_type: type) -> type:
        """Nearest registered base, so EnemySpriteVu lands in the sprite
        group without a second registration. Cached per concrete type so the
        mro walk happens once."""
        route = self._routes.get(vu_type)
        if route is not None:
            return route
        for base in vu_type.__mro__:
            if base in self.factories:
                self._routes[vu_type] = base
                return base
        raise KeyError(
            f"No vu group registered for {vu_type.__name__}. "
            f"Register one, or set groupable = False on the type."
        )

    def group_for(self, vu: Vu) -> VuGroup:
        route = self.route_for(type(vu))
        groups = self.groups[route]
        for group in groups:
            if not group.full:
                return group

        group = self.factories[route]()
        groups.append(group)
        logger.debug(f"{self}: spilled into {group} for {route.__name__}")
        if self._device_ready:
            group.ensure_created()
        return group

    def groups_flat(self) -> Iterator[VuGroup]:
        for groups in self.groups.values():
            yield from groups

    # -- membership --------------------------------------------------------

    def append(self, vu: Vu) -> None:
        if vu.group is not None:
            # Checked here, not in VuGroup. Per-group membership stops
            # catching duplicates as soon as spill exists: once the first
            # group is full, routing hands the duplicate to a second group
            # that has never seen it, and it draws twice. For a grid this is
            # the signal that a node sits in two cells.
            raise ValueError(f"{vu} already in {vu.group}")

        # Assigned before routing, so it is global across every group and
        # independent of which one the vu lands in.
        vu.group_sequence = self._next_sequence
        self._next_sequence += 1

        self.group_for(vu).append(vu)
        self._replan = True

    def extend(self, vus) -> None:
        for vu in vus:
            self.append(vu)

    def remove(self, vu: Vu) -> None:
        group = vu.group
        if group is None:
            logger.warning(f"{vu} has no group; searching members")
            for candidate in self.groups_flat():
                if vu in candidate.members:
                    group = candidate
                    break
        if group is None:
            return
        group.remove(vu)
        self._replan = True

    '''
    def remove(self, vu: Vu) -> None:
        group = vu.group
        if group is None:
            return
        group.remove(vu)
        # No reindexing loop. Slots are assigned wholesale by replan, so a
        # removal only has to invalidate the plan.
        self._replan = True
    '''

    def clear(self) -> None:
        for group in self.groups_flat():
            group.clear()
        self.plan.clear()
        self._replan = False
        # _next_sequence deliberately keeps climbing. It only has to be
        # monotonic within one plan, and resetting it buys nothing.

    def invalidate(self) -> None:
        """Order changed; the plan is stale.

        Coalesced — however many times this is called between updates, the
        replan happens once.
        """
        self._replan = True

    # -- lifetime ----------------------------------------------------------

    def _create(self) -> None:
        super()._create()
        self._device_ready = True
        for group in self.groups_flat():
            group.ensure_created()

    def _destroy(self) -> None:
        for group in self.groups_flat():
            group.destroy()
        self.groups.clear()
        self.plan.clear()
        self._device_ready = False
        super()._destroy()

    # -- frame -------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        for group in self.groups_flat():
            group.update(delta_time)
        if self._replan:
            self.replan()

    def replan(self) -> None:
        entries: list[tuple[Any, VuGroup, Vu]] = []
        deferred = 0

        for group in self.groups_flat():
            for vu in group.members:
                if not group.ready(vu):
                    # Model hasn't landed. No slot, no run, no draw.
                    vu.node_buffer_index = -1
                    deferred += 1
                    continue
                entries.append((group.sort_key(vu), group, vu))

        # Stable, and the key is first in the tuple so groups and vus are
        # never compared. Collection order above is per group, so the key
        # has to carry the whole global ordering on its own — which is what
        # the append sequence in it is for.
        entries.sort(key=lambda entry: entry[0])

        cursors: dict[VuGroup, int] = {}
        self.plan.clear()
        run: Run = None
        run_group: VuGroup = None

        for _, group, vu in entries:
            slot = cursors.get(group, 0)
            cursors[group] = slot + 1
            group.place(vu, slot)

            # Contiguity is necessary but not sufficient: two slots can be
            # adjacent in the buffer and still need separate draws, because
            # something from another group sorted between them.
            if run is not None and run_group is group and group.extends(run, vu):
                run.count += 1
            else:
                run = group.new_run(vu, slot)
                run_group = group
                self.plan.append((group, run))

        # Anything deferred retries next update. The cost is a re-sort per
        # frame while a model is still loading, which is what the old
        # _rebatch flag did too. The real fix is a signal from the vu when
        # its model arrives; worth doing if loading ever spans many frames.
        self._replan = deferred > 0

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        if not self.plan:
            return
        renderer = Renderer.get_current()
        state = RenderState(renderer.pass_enc)
        for group, run in self.plan:
            group.draw_run(state, run)

    def __repr__(self) -> str:
        total = sum(len(group) for group in self.groups_flat())
        group_count = sum(len(groups) for groups in self.groups.values())
        return (
            f"<RenderGroup: {total} vus in {group_count} groups, "
            f"{len(self.plan)} draws>"
        )