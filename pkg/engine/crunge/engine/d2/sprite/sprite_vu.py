from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ...uniforms import cast_matrix4
from ...renderer import Renderer

from ..node_2d import Node2D
from ..vu_2d import Vu2D
from ..uniforms_2d import NodeUniform

from .sprite_program import SpriteProgram
from .sprite import Sprite, SpriteMembership


if TYPE_CHECKING:
    from .sprite_vu_group import SpriteVuGroup

class SpriteVu(Vu2D):
    group: "SpriteVuGroup"
    
    def __init__(self, sprite: Sprite = None) -> None:
        super().__init__()
        self.sprite_membership: SpriteMembership = None
        self.sprite = sprite

    @property
    def sprite(self) -> Sprite:
        return self.sprite_membership.member if self.sprite_membership is not None else None

    @sprite.setter
    def sprite(self, sprite: Sprite):
        if sprite is None:
            return

        sprite_group = self.group.sprite_group if self.group is not None else None
        self.sprite_membership = sprite.join(sprite_group)

        if self.enabled:
            self.update_gpu()

    def on_group(self) -> None:
        self.sprite_membership = self.sprite.join(self.group.sprite_group)

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
        # logger.debug(f"SpriteVu: on_node_model_change: {node.model}")
        self.sprite = node.model

    def create_program(self):
        self.program = SpriteProgram()

    def update_gpu(self):
        uniform = NodeUniform()
        uniform.transform.data = cast_matrix4(self.transform)

        if self.sprite_membership is not None:
            uniform.model_index = self.sprite_membership.index

        # logger.debug(f"SpriteVu: update_gpu: {uniform.model_index}")
        self.node_buffer[self.node_buffer_index] = uniform

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self.sprite.bind(pass_enc, self.sprite_membership)

    def draw(self, renderer: Renderer) -> None:
        if not self.manual_draw:
            return

        frustum = renderer.camera_2d.frustum
        if not self.bounds.intersects(frustum):
            # logger.debug(f"SpriteVu: {self} is not in frustum: {frustum}")
            return

        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4)
