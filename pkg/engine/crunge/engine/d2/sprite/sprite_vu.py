from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ...uniforms import cast_matrix4, cast_vec4, cast_vec2, cast_tuple4f
from ...renderer import Renderer
from ...buffer import UniformBuffer

from ..node_2d import Node2D
from ..vu_2d import Vu2D
from ..uniforms_2d import NodeUniform
from ..binding_2d import NodeBindGroup

from .sprite_program import SpriteProgram
from .sprite import Sprite

if TYPE_CHECKING:
    from .sprite_vu_group import SpriteVuGroup


class SpriteVu(Vu2D):
    def __init__(self, sprite: Sprite = None) -> None:
        super().__init__()
        self._sprite = sprite

        '''
        self.group: "SpriteVuGroup" = None
        self.program: SpriteProgram = None
        self.manual_draw = True

        self.bind_group: NodeBindGroup = None
        self.buffer: UniformBuffer[NodeUniform] = None
        self._buffer_index = 0
        '''

    @property
    def sprite(self) -> Sprite:
        return self._sprite
    
    @sprite.setter
    def sprite(self, value: Sprite):
        self._sprite = value
        if self.enabled:
            self.update_gpu()
    
    '''
    @property
    def buffer_index(self) -> int:
        return self._buffer_index

    @buffer_index.setter
    def buffer_index(self, value: int):
        self._buffer_index = value
        self.on_transform()
    '''

    @property
    def size(self) -> glm.vec2:
        if self.sprite is None:
            return glm.vec2(1.0)
        return glm.vec2(self.sprite.rect.size)

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    def on_node_model_change(self, node: Node2D) -> None:
        super().on_node_model_change(node)
        #logger.debug(f"SpriteVu: on_node_model_change: {node.model}")
        self.sprite = node.model

    '''
    def _create(self):
        super()._create()
        group = self.group
        if group is not None:
            group.append(self)
            if group.is_render_group:
                self.manual_draw = False

        if not self.manual_draw:
            return

        self.create_program()
        self.create_buffer()
        self.create_bind_group()
    '''

    '''
    def destroy(self):
        if self.group is not None:
            self.group.remove(self)
        super().destroy()
    '''

    """
    def __del__(self):
        if self.group is not None:
            self.group.remove(self)
    """

    def create_program(self):
        self.program = SpriteProgram()

    '''
    def create_buffer(self):
        self.buffer = UniformBuffer(NodeUniform, 1, label="Sprite Node Buffer")

    def create_bind_group(self):
        self.bind_group = NodeBindGroup(
            self.buffer.get(),
            self.buffer.size,
        )
    '''

    '''
    def on_transform(self) -> None:
        super().on_transform()
        if self.enabled:
            self.update_gpu()

    def update_gpu(self):
        uniform = NodeUniform()
        uniform.transform.data = cast_matrix4(self.transform)

        self.buffer[self.buffer_index] = uniform

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.sprite.bind(pass_enc)
        self.bind_group.bind(pass_enc)
    '''

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self.sprite.bind(pass_enc)

    def draw(self, renderer: Renderer) -> None:
        if not self.manual_draw:
            return
        
        frustum = renderer.camera_2d.frustum
        if not self.bounds.intersects(frustum):
            #logger.debug(f"SpriteVu: {self} is not in frustum: {frustum}")
            return
        
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        pass_enc.draw(4)
