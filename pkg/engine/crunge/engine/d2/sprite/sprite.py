from loguru import logger

from crunge import wgpu

from ...math import Size2
from ...buffer import UniformBuffer

from ..renderer_2d import Renderer2D
from ..vu_2d import Vu2D
from ..uniforms_2d import (
    cast_matrix4,
    ModelUniform,
)

from .sprite_program import SpriteProgram
from .sprite_material import SpriteMaterial


class Sprite(Vu2D):
    def __init__(self, material: SpriteMaterial) -> None:
        super().__init__()
        self.material = material

        self.model_bind_group: wgpu.BindGroup = None
        self.model_uniform_buffer = UniformBuffer(ModelUniform, 1, label="Sprite Model Buffer")
        logger.debug(f"Model Uniform Buffer: {self.model_uniform_buffer}")

        self.program = SpriteProgram()
        self.create_bind_groups()

    @property
    def size(self) -> Size2:
        #return self.texture.size
        return Size2(self.width, self.height)

    @property
    def width(self) -> int:
        return self.material.texture.width

    @property
    def height(self) -> int:
        return self.material.texture.height

    def create_bind_groups(self):
        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.model_uniform_buffer.get(),
                    size=self.model_uniform_buffer.size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bind_group_desc)

    def on_transform(self):
        super().on_transform()
        '''
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.model_uniform_buffer[0] = model_uniform
        '''
        self.model_uniform_buffer[0].transform.data = cast_matrix4(self.transform)
        self.model_uniform_buffer.upload()

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.pipeline)
        self.material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.model_bind_group)

    def draw(self, renderer: Renderer2D):
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        '''
        pass_enc.set_pipeline(self.program.pipeline)
        #pass_enc.set_bind_group(1, self.material_bind_group)
        self.material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.model_bind_group)
        '''
        self.bind(pass_enc)
        pass_enc.draw(4)
