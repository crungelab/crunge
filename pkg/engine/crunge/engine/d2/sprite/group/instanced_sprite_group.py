from loguru import logger

from crunge import wgpu

from ....renderer import Renderer
from ....buffer import UniformBuffer

from ...uniforms_2d import (
    ModelUniform,
)

from ..sprite_material import SpriteMaterial
from ..sprite import Sprite

from .sprite_group import SpriteGroup
from .instanced_sprite_group_program import InstancedSpriteGroupProgram

ELEMENTS = 32


class InstancedSpriteBatch:
    def __init__(self, material: SpriteMaterial, instance_count: int, first_instance: int) -> None:
        self.material = material
        self.instance_count = instance_count
        self.first_instance = first_instance


class InstancedSpriteGroup(SpriteGroup):
    def __init__(self, size: int = ELEMENTS) -> None:
        super().__init__()
        self.is_render_group = True
        self.size = size
        self.batches: list[InstancedSpriteBatch] = []

        self.bind_group: wgpu.BindGroup = None
        # self.buffer = UniformBuffer(ModelUniform, size, label="SpriteRenderGroup Buffer")
        self.buffer = UniformBuffer(
            ModelUniform,
            size,
            wgpu.BufferUsage.STORAGE,
            label="SpriteRenderGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.buffer}")

        self.program = InstancedSpriteGroupProgram()
        self.create_bind_group()

    def append(self, sprite: Sprite) -> None:
        super().append(sprite)
        sprite.buffer = self.buffer
        sprite.buffer_index = len(self.members) - 1
        self.batch()

    def batch(self):
        for member in self.members:
            if len(self.batches) == 0 or self.batches[-1].material != member.material:
                self.batches.append(
                    InstancedSpriteBatch(member.material, 1, member.buffer_index)
                )
            else:
                self.batches[-1].instance_count += 1

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
    def draw(self, renderer: Renderer):
        if len(self.batches) == 0:
            return
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for batch in self.batches:
            batch.material.bind(pass_enc)
            pass_enc.draw(4, batch.instance_count, 0, batch.first_instance)