from loguru import logger

from ....renderer import Renderer

from ..sprite_vu import SpriteVu
from ..sprite_group import SpriteGroup
from ..dynamic import DynamicSpriteVuGroup

from .instanced_sprite_program import InstancedSpriteProgram

ELEMENTS = 32


class InstancedSpriteVuBatch:
    """A contiguous run of instances sharing one texture."""

    def __init__(self, sprite_vu: SpriteVu, first_instance: int) -> None:
        self.sprite_vu = sprite_vu
        self.first_instance = first_instance
        self.instance_count = 1

    def __repr__(self) -> str:
        return (
            f"Batch(first={self.first_instance}, count={self.instance_count})"
        )

    @property
    def next_instance(self) -> int:
        return self.first_instance + self.instance_count

    def draw(self):
        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        self.sprite_vu.sprite.bind(pass_enc, self.sprite_vu.sprite_membership)
        pass_enc.draw(4, self.instance_count, 0, self.first_instance)


class InstancedSpriteVuGroup(DynamicSpriteVuGroup):
    """Batches its members by texture, preserving member order.

    Two properties callers depend on:

    * **Member order is draw order.** Within one instanced draw call instances
      rasterize by ascending instance index, and blending follows that order.
      A caller that appends back to front gets painter's algorithm for free --
      but only if instance indices ascend with member order, which is what
      `reindex` guarantees. Slots handed out at sprite creation time reflect
      allocation order, not member order.
    * **Batches only merge across contiguous slots.** A batch draws
      `[first_instance, first_instance + instance_count)`. If two members share
      a texture but not adjacent slots, merging them would draw whatever sits
      between them. `batch_all` starts a new batch instead.

    A vu may be appended before its sprite arrives, so batching has the same
    not-ready-yet problem as a vu's own upload, and the same answer: skip,
    mark, rebuild later. `_draw` consumes the mark as well as `update`, so a
    group excluded from the update traversal still recovers.
    """

    def __init__(self, count: int = ELEMENTS, sprite_group: SpriteGroup = None) -> None:
        super().__init__(count, sprite_group)
        self.is_render_group = True
        self.batches: list[InstancedSpriteVuBatch] = []
        self._rebatch = False
        self.program = InstancedSpriteProgram()

    # ------------------------------------------------------------------
    # Membership
    # ------------------------------------------------------------------

    def clear(self):
        super().clear()
        self.batches.clear()
        self._rebatch = False

    def append(self, vu: SpriteVu) -> None:
        """Add a member. Batching is deferred.

        The old incremental `batch(vu)` on append was unsound once reindexing
        entered the picture: it read `node_buffer_index` before reindex had
        assigned the final slot.
        """
        super().append(vu)
        self._rebatch = True

    def remove(self, vu):
        super().remove(vu)
        self._rebatch = True

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def reindex(self) -> None:
        """Make instance slots match member order.

        No-op when the allocator already handed out slots in append order; the
        cost is one comparison per member. Where it is not a no-op -- a vu
        created long before it was appended, a rebuilt stream, a free-list
        allocator -- this is the step that makes draw order mean anything.
        """
        moved = 0
        for index, member in enumerate(self.members):
            if member.node_buffer_index == index:
                continue
            member.node_buffer_index = index
            # ASSUMPTION: this is what forces the model data to be rewritten
            # at the new slot before the next draw. If DynamicSpriteGroup
            # tracks dirtiness differently, this is the line to change --
            # without it the sprite's transform stays at its old index.
            member.mark_dirty()
            moved += 1

        if moved:
            self._rebatch = True
            logger.debug(f"reindex: {moved}/{len(self.members)} slots moved")

    # ------------------------------------------------------------------
    # Batching
    # ------------------------------------------------------------------

    def rebatch(self) -> None:
        """Rebuild batches now, regardless of the pending mark."""
        self.batch_all()

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        if self._rebatch:
            self.batch_all()

    def batch_all(self):
        self.batches.clear()
        # Cleared first; the loop sets it again for any member still waiting.
        self._rebatch = False

        for member in self.members:
            if member.sprite is None:
                # Sprite has not landed yet. Come back for it.
                self._rebatch = True
                continue

            last = self.batches[-1] if self.batches else None
            index = member.node_buffer_index

            # TODO: compare by texture until materials are registered
            if (
                last is not None
                and last.sprite_vu.sprite.texture is member.sprite.texture
                and index == last.next_instance
            ):
                last.instance_count += 1
            else:
                self.batches.append(InstancedSpriteVuBatch(member, index))

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def _draw(self):
        if self._rebatch:
            self.batch_all()

        if not self.batches:
            return

        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)

        for batch in self.batches:
            batch.draw()

        super()._draw()