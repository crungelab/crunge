from loguru import logger

from ....renderer import Renderer

from ..sprite_vu import SpriteVu

from .buffered_sprite_vu_group import BufferedSpriteVuGroup
from .instanced_sprite_program import InstancedSpriteProgram

ELEMENTS = 32


class InstancedSpriteVuBatch:
    def __init__(self, sprite_vu: SpriteVu, first_instance: int) -> None:
        self.sprite_vu = sprite_vu
        self.first_instance = first_instance
        self.instance_count = 1

    def draw(self, renderer: Renderer):
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.sprite_vu.sprite.bind(pass_enc)
        pass_enc.draw(4, self.instance_count, 0, self.first_instance)

class InstancedSpriteVuGroup(BufferedSpriteVuGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__(count)
        self.is_render_group = True
        self.batches: list[InstancedSpriteVuBatch] = []
        self.program = InstancedSpriteProgram()

    def clear(self):
        super().clear()
        self.batches.clear()

    def append(self, vu: SpriteVu) -> None:
        super().append(vu)
        self.batch(vu)

    def remove(self, vu):
        super().remove(vu)
        self.batch_all()

    def batch(self, member: SpriteVu):
        # Compare by texture until I start registering materials
        if len(self.batches) == 0 or self.batches[-1].sprite_vu.sprite.texture != member.sprite.texture:
            self.batches.append(
                InstancedSpriteVuBatch(member, member.buffer_index)
            )
        else:
            self.batches[-1].instance_count += 1

    def batch_all(self):
        self.batches.clear()
        for member in self.visuals:
            self.batch(member)

    def draw(self, renderer: Renderer):
        if len(self.batches) == 0:
            return
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for batch in self.batches:
            batch.draw(renderer)
