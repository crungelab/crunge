from typing import TYPE_CHECKING

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
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self.bounds = Bounds2()

        self.node_bind_group: NodeBindGroup = None
        self.node_buffer: UniformBuffer[NodeUniform] = None
        self._node_buffer_index = 0

        self.group: "VuGroup" = None
        self.program: Program2D = None
        self.manual_draw = True

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
        self.create_buffers()
        self.create_bind_groups()

    def destroy(self):
        if self.group is not None:
            self.group.remove(self)
        super().destroy()

    def create_buffers(self):
        self.node_buffer = UniformBuffer(NodeUniform, 1, label="Sprite Node Buffer")

    def create_bind_groups(self):
        self.node_bind_group = NodeBindGroup(
            self.node_buffer.get(),
            self.node_buffer.size,
        )

    def create_program(self):
        pass

    @property
    def node_buffer_index(self) -> int:
        return self._node_buffer_index

    @node_buffer_index.setter
    def node_buffer_index(self, value: int):
        self._node_buffer_index = value
        self.on_transform()

    @property
    def transform(self) -> glm.mat4:
        return self._transform
    
    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_transform(self) -> None:
        if self.enabled:
            self.update_gpu()

    '''
    def on_transform(self):
        pass
    '''

    @property
    def size(self) -> glm.vec2:
        raise NotImplementedError

    def on_node_transform_change(self, node: Node2D) -> None:
        matrix = glm.mat4(1.0)  # Identity matrix
        #matrix = glm.translate(matrix, glm.vec3(x, y, z))
        #matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self.size.x , self.size.y, 1),
        )

        self.transform = node.transform * matrix
        #logger.debug(f"Vu2D: {self.transform}")
        self.bounds = node.bounds

    def update_gpu(self):
        uniform = NodeUniform()
        uniform.transform.data = cast_matrix4(self.transform)

        self.node_buffer[self.node_buffer_index] = uniform

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.node_bind_group.bind(pass_enc)
