from typing import TYPE_CHECKING

from crunge.engine import colors
from loguru import logger
import glm

from crunge import wgpu

from ..math import Bounds2
from ..uniforms import cast_matrix4, cast_vec4, cast_vec2, cast_tuple4f

from ..vu import Vu
from ..buffer import UniformBuffer

from .node_2d import Node2D

from .uniforms_2d import NodeUniform
from .binding_2d import NodeBindGroup
from .program_2d import Program2D

if TYPE_CHECKING:
    from ..vu_group import VuGroup


class Vu2D(Vu[Node2D]):
    """Base for 2D vus.

    Owns the node uniform. Every setter that feeds it marks GPU dirt rather
    than writing; the write happens in `_flush_gpu`, driven from `update`
    before the render pass opens. A grouped vu does not own its buffer —
    the group assigns `node_buffer` and `node_buffer_index` at append time,
    which can happen after the vu is enabled. The flush guards on that and
    retries, so the two orders are equivalent.
    """

    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self._color = glm.vec4(1.0, 1.0, 1.0, 1.0)
        self.bounds = Bounds2()

        self.node_bind_group: NodeBindGroup = None
        self.node_buffer: UniformBuffer[NodeUniform] = None
        self._node_buffer_index = 0

        self._group: "VuGroup" = None
        self.program: Program2D = None
        self.manual_draw = True

    # -- lifetime ----------------------------------------------------------

    def _create(self):
        super()._create()
        group = self.group
        if group is not None:
            if group.is_render_group:
                self.manual_draw = False

    def _destroy(self):
        if self.group is not None:
            self.group.remove(self)
        super()._destroy()

    def _enable(self) -> None:
        # Vu._enable subscribes and syncs, which marks dirt. The buffers it
        # will be written into are created below; the write itself waits for
        # the next flush, so the order here is safe either way.
        super()._enable()
        if not self.manual_draw:
            return
        self.create_program()
        self.create_buffers()
        self.create_bind_groups()
        self.mark_gpu()

    def create_buffers(self):
        self.node_buffer = UniformBuffer(NodeUniform, 1, label="Sprite Node Buffer")

    def create_bind_groups(self):
        self.node_bind_group = NodeBindGroup(
            self.node_buffer.get(),
            self.node_buffer.size,
        )

    def create_program(self):
        pass

    # -- group -------------------------------------------------------------

    @property
    def group(self) -> "VuGroup":
        return self._group

    @group.setter
    def group(self, value: "VuGroup"):
        self._group = value
        self.on_group()

    def on_group(self) -> None:
        pass

    @property
    def node_buffer_index(self) -> int:
        return self._node_buffer_index

    @node_buffer_index.setter
    def node_buffer_index(self, value: int):
        self._node_buffer_index = value
        self.on_transform()

    # -- transform and colour ---------------------------------------------

    @property
    def transform(self) -> glm.mat4:
        return self._transform

    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_transform(self) -> None:
        self.mark_gpu()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.mark_gpu()

    @property
    def size(self) -> glm.vec2:
        raise NotImplementedError

    def on_transform_changed(self, node: Node2D) -> None:
        matrix = glm.mat4(1.0)  # Identity matrix
        # matrix = glm.translate(matrix, glm.vec3(x, y, z))
        # matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self.size.x, self.size.y, 1),
        )

        self.transform = node.transform * matrix
        self.bounds = node.bounds

    # -- deferred rebuild --------------------------------------------------

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.flush()

    def update_gpu(self) -> None:
        """Deferred alias, kept so older callers keep working. Delete once
        `rg update_gpu` comes back clean."""
        self.mark_gpu()

    def build_uniform(self) -> NodeUniform:
        """Override point for subclasses with more to say. Head-call super,
        set the extra fields, return it."""
        uniform = NodeUniform()
        uniform.transform.data = cast_matrix4(self.transform)
        uniform.color = cast_tuple4f(self.color)
        return uniform

    def _flush_gpu(self) -> bool:
        if self.node_buffer is None:
            return False  # grouped vu, not appended yet; retry next frame
        self.node_buffer[self.node_buffer_index] = self.build_uniform()
        return True

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        self.node_bind_group.bind(pass_enc)

    # -- draw --------------------------------------------------------------
    def draw(self) -> None:
        if not self.manual_draw:
            return  # a render group draws us; we have no program of our own
        self._draw()
