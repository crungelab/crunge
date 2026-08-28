from loguru import logger

from ....renderer import Renderer

from ..sprite_vu import SpriteVu
from ..sprite_group import SpriteGroup
from ..dynamic import DynamicSpriteVuGroup

from .instanced_sprite_program import InstancedSpriteProgram

ELEMENTS = 32


class InstancedSpriteVuBatch:
    def __init__(self, sprite_vu: SpriteVu, first_instance: int) -> None:
        self.sprite_vu = sprite_vu
        self.first_instance = first_instance
        self.instance_count = 1

    def draw(self):
        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        self.sprite_vu.sprite.bind(pass_enc, self.sprite_vu.sprite_membership)
        pass_enc.draw(4, self.instance_count, 0, self.first_instance)


class InstancedSpriteVuGroup(DynamicSpriteVuGroup):
    """Batches its members by texture.

    A vu can be appended before its model arrives, so batching has the same
    not-ready-yet problem as a vu's own upload, and the same answer: skip,
    mark, rebuild on the next update. Without the rebuild a vu that was
    appended sprite-less never enters a batch and silently never draws.
    """

    def __init__(self, count: int = ELEMENTS, sprite_group: SpriteGroup = None) -> None:
        super().__init__(count, sprite_group)
        self.is_render_group = True
        self.batches: list[InstancedSpriteVuBatch] = []
        self._rebatch = False
        self.program = InstancedSpriteProgram()

    def clear(self):
        super().clear()
        self.batches.clear()
        self._rebatch = False

    def append(self, vu: SpriteVu) -> None:
        super().append(vu)
        self.batch(vu)

    def remove(self, vu):
        super().remove(vu)
        self.batch_all()

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        if self._rebatch:
            self.batch_all()

    def batch(self, member: SpriteVu):
        if member.sprite is None:
            # Model has not landed yet. Rebuild once it has.
            self._rebatch = True
            return

        # TODO: Compare by texture until I start registering materials
        if (
            len(self.batches) == 0
            or self.batches[-1].sprite_vu.sprite.texture != member.sprite.texture
        ):
            self.batches.append(
                InstancedSpriteVuBatch(member, member.node_buffer_index)
            )
        else:
            self.batches[-1].instance_count += 1

    def batch_all(self):
        self.batches.clear()
        # Cleared first; batch() sets it again for any member still waiting.
        self._rebatch = False
        for member in self.visuals:
            self.batch(member)

    def _draw(self):
        if len(self.batches) == 0:
            return
        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        for batch in self.batches:
            batch.draw()