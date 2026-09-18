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
    the group assigns `node_buffer` at append time and the RenderGroup
    assigns `node_buffer_index` at replan, both of which can happen after
    the vu is enabled. The flush guards on each and retries, so the orders
    are equivalent.

    `groupable`, `is_grouped`, `find_render_group` and group membership all
    live on Vu. What is left here is the half that membership decides: an
    ungrouped vu allocates its own buffer and bind group and draws itself;
    a grouped one does neither.
    """

    # Sentinel for "grouped, but the plan has not placed me yet". A real
    # index, including 0, means the slot is mine to write.
    UNPLACED = -1

    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self._color = glm.vec4(1.0, 1.0, 1.0, 1.0)
        self.bounds = Bounds2()

        self.node_bind_group: NodeBindGroup = None
        self.node_buffer: UniformBuffer[NodeUniform] = None
        self._node_buffer_index = 0
        self._sort_key = 0.0

        self.program: Program2D = None

    # -- lifetime ----------------------------------------------------------

    def plug(self) -> None:
        super().plug()
        self.node._mark_bounds_dirty()

    def _enable(self) -> None:
        # Head call: Vu._enable subscribes, syncs, and settles membership,
        # so is_grouped is answered by the time it returns. The dirt marked
        # by sync waits for the next flush either way.
        super()._enable()

        if self.is_grouped:
            return

        self.create_program()
        self.create_buffers()
        self.create_bind_groups()
        self.mark_gpu()

    def _disable(self) -> None:
        # Checked before super(), which frees the slot and clears the render
        # group — after that there is no way to tell whether the buffer was
        # ours to release or the group's.
        if not self.is_grouped:
            self.destroy_buffers()
        super()._disable()

    def create_buffers(self):
        self.node_buffer = UniformBuffer(NodeUniform, 1, label="Sprite Node Buffer")
        self._node_buffer_index = 0

    def create_bind_groups(self):
        self.node_bind_group = NodeBindGroup(
            self.node_buffer.get(),
            self.node_buffer.size,
        )

    def destroy_buffers(self):
        """Mirror of create_buffers/create_bind_groups.

        Was missing, so a vu that enabled, disabled and re-enabled leaked
        the first allocation — and under gc.disable() it never came back.
        """
        self.node_bind_group = None
        self.node_buffer = None
        self.program = None

    def create_program(self):
        pass

    # -- group -------------------------------------------------------------

    @property
    def node_buffer_index(self) -> int:
        return self._node_buffer_index

    @node_buffer_index.setter
    def node_buffer_index(self, value: int):
        self._node_buffer_index = value
        # Marks dirt, so the uniform written before the slot was known is
        # retried into the right place on the next flush.
        self.on_transform()

    @property
    def is_placed(self) -> bool:
        return self._node_buffer_index >= 0

    @property
    def sort_key(self) -> float:
        """Global draw order. Lower draws first.

        Settable rather than derived, because what a 2D vu sorts by is the
        caller's business: a grid supplies a projected depth, a flat layer
        leaves it at 0 and lets the stable sort preserve insertion order.
        """
        return self._sort_key

    @sort_key.setter
    def sort_key(self, value: float) -> None:
        if value == self._sort_key:
            return
        self._sort_key = value
        # Order is the RenderGroup's plan, not the buffer's contents, so
        # mark_gpu is the wrong signal here — nothing in the uniform
        # changed. Without this the plan keeps the old order until some
        # unrelated append happens to invalidate it.
        render_group = self.render_group
        if render_group is not None:
            render_group.invalidate()

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

        self.transform = node.global_transform * matrix
        self.bounds = node.global_bounds

    # -- deferred rebuild --------------------------------------------------

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.flush()

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
        if not self.is_placed:
            # Appended but not yet placed by a replan, or removed. -1 is a
            # valid Python index, so without this guard the write lands on
            # the last slot and silently corrupts whoever owns it.
            return False
        self.node_buffer[self._node_buffer_index] = self.build_uniform()
        return True

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        self.node_bind_group.bind(pass_enc)

    def draw(self) -> None:
        # A grouped vu is still in its node's _drawables bucket, so this is
        # called every frame and has to decline. Silent rather than raising:
        # the arrangement is legitimate, not a mistake to catch.
        if self.is_grouped:
            return
        self._draw()