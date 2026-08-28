from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ...math import Bounds2
from ...uniforms import cast_matrix4, cast_vec4, cast_tuple4f
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
        # Held directly rather than read back through the membership, so a
        # regroup can rejoin without needing the membership it is replacing.
        self._sprite: Sprite = None
        self.sprite_membership: SpriteMembership = None
        self.sprite = sprite

    # -- sprite ------------------------------------------------------------

    @property
    def sprite(self) -> Sprite:
        return self._sprite

    @sprite.setter
    def sprite(self, sprite: Sprite) -> None:
        if sprite is None or sprite is self._sprite:
            return
        self._sprite = sprite
        self.join()
        self.mark_gpu()

    def join(self) -> None:
        """(Re)join the group's sprite group. Tolerates either half being
        absent — whichever of sprite/group arrives second calls this again."""
        if self._sprite is None:
            return
        sprite_group = self.group.sprite_group if self.group is not None else None
        self.sprite_membership = self._sprite.join(sprite_group)

    def on_group(self) -> None:
        self.join()
        self.mark_gpu()

    @property
    def size(self) -> glm.vec2:
        if self._sprite is None:
            return glm.vec2(1.0)
        return glm.vec2(self._sprite.size)

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    def on_model_changed(self, node: Node2D) -> None:
        super().on_model_changed(node)
        self.sprite = node.model

    def create_program(self):
        logger.debug("SpriteVu: create_program")
        self.program = SpriteProgram()

    # -- uniform -----------------------------------------------------------

    def build_uniform(self) -> NodeUniform:
        uniform = super().build_uniform()
        if self.sprite_membership is not None:
            uniform.model_index = self.sprite_membership.index
        return uniform

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self._sprite.bind(pass_enc, self.sprite_membership)

    def _draw(self) -> None:
        if self._sprite is None or self.sprite_membership is None:
            return

        renderer = Renderer.get_current()

        frustum = renderer.camera_2d.frustum

        if not self.bounds.intersects(frustum):
            return

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4)

    def update_transform(
        self,
        position: glm.vec3,
        size: glm.vec2,
        rotation=0.0,
        scale=glm.vec3(1, 1, 1),
        depth=0.0,
    ):
        x = position.x
        y = position.y
        z = depth

        model = glm.mat4(1.0)  # Identity matrix
        model = glm.translate(model, glm.vec3(x, y, z))
        model = glm.scale(
            model,
            glm.vec3(size.x * scale.x, size.y * scale.y, 1),
        )
        self.transform = model

        self.bounds = Bounds2(
            x - size.x / 2,
            y - size.y / 2,
            size.x,
            size.y,
        )
