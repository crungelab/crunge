from loguru import logger

from crunge import wgpu

from ....renderer import Renderer
from ....buffer import UniformBuffer

from ...uniforms_2d import (
    ModelUniform,
)

from ..sprite import Sprite
from ..sprite_vu import SpriteVu

from .sprite_vu_group import SpriteVuGroup
from .instanced_sprite_vu_group_program import InstancedSpriteVuGroupProgram

ELEMENTS = 32


class InstancedSpriteVuBatch:
    def __init__(self, sprite_vu: SpriteVu, first_instance: int) -> None:
        self.sprite_vu = sprite_vu
        self.first_instance = first_instance
        self.instance_count = 1


class InstancedSpriteVuGroup(SpriteVuGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_render_group = True
        self.count = count
        self.batches: list[InstancedSpriteVuBatch] = []

        self.bind_group: wgpu.BindGroup = None
        # self.buffer = UniformBuffer(ModelUniform, size, label="SpriteRenderGroup Buffer")
        self.buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="SpriteRenderGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.buffer}")

        self.program = InstancedSpriteVuGroupProgram()
        self.create_bind_group()

    def clear(self):
        super().clear()
        self.batches.clear()

    def append(self, sprite: SpriteVu) -> None:
        super().append(sprite)
        sprite.buffer = self.buffer
        sprite.buffer_index = len(self.members) - 1
        #self.batch_all()
        self.batch(sprite)

    def remove(self, vu):
        super().remove(vu)
        self.batch_all()

    def batch(self, member: SpriteVu):
        # Compare by texture until I start registering materials
        if len(self.batches) == 0 or self.batches[-1].sprite_vu.sprite.texture != member.sprite.texture:
            self.batches.append(
                #InstancedSpriteBatch(member.sprite, member.buffer_index)
                InstancedSpriteVuBatch(member, member.buffer_index)
            )
        else:
            self.batches[-1].instance_count += 1

    def batch_all(self):
        self.batches.clear()
        for member in self.members:
            self.batch(member)

    '''
    def batch_all(self):
        self.batches.clear()
        for member in self.members:
        #for i, member in enumerate(self.members):
            #member.buffer_index = i
            # Hack this until I start registering materials
            if len(self.batches) == 0 or self.batches[-1].material.texture != member.material.texture:
            #if len(self.batches) == 0 or self.batches[-1].material != member.material:
                self.batches.append(
                    #InstancedSpriteBatch(member.material, i)
                    InstancedSpriteBatch(member.material, member.buffer_index)
                )
            else:
                self.batches[-1].instance_count += 1

        logger.debug(f"Batched {len(self.batches)} batches")
    '''

    '''
    def batch(self):
        self.batches.clear()
        for member in self.members:
            if len(self.batches) == 0 or self.batches[-1].material != member.material:
                self.batches.append(
                    InstancedSpriteBatch(member.material, 1, member.buffer_index)
                )
            else:
                self.batches[-1].instance_count += 1
    '''

    def create_bind_group(self):
        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.buffer.get(),
                    size=self.buffer.size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(model_bind_group_desc)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.pipeline)
        # self.material.bind(pass_enc)
        #self.members[0].material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.bind_group)

    def draw(self, renderer: Renderer):
        if len(self.batches) == 0:
            return
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for batch in self.batches:
            batch.sprite_vu.sprite.bind(pass_enc)
            pass_enc.draw(4, batch.instance_count, 0, batch.first_instance)

    '''
    def draw(self, renderer: Renderer):
        if len(self.members) == 0:
            return
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        # logger.debug(f"Drawing {len(self.members)} sprites")
        # exit()
        pass_enc.draw(4, len(self.members))
    '''
