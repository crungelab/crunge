from typing import Callable, List, TYPE_CHECKING
from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass

from crunge import wgpu

from ..viewport import Viewport, ViewportListener
from ..uniforms import cast_vec3, cast_matrix4
from ..binding import SceneBindGroup

if TYPE_CHECKING:
    from .renderer_3d import Renderer3D
from .node_3d import Node3D
from .vu_3d import Vu3D
from .uniforms_3d import (
    CameraUniform,
)
from .program_3d import Program3D


DrawCallback = Callable[["Renderer3D"], None]


class DeferredDraw:
    def __init__(self, vu: Vu3D, callback: DrawCallback):
        self.vu = vu
        self.node = vu.node
        self.callback = callback


@klass.singleton
class CameraProgram3D(Program3D):
    pass


class Camera3D(Node3D, ViewportListener):
    def __init__(
        self,
        viewport_size=glm.vec2(1024, 768),
        position=glm.vec3(0.0, 0.0, 4.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        near=0.1,
        far=100.0,
    ):
        super().__init__(position)
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)
        self.zoom = 45.0

        self.up = up
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self._near = near
        self._far = far

        self._viewport: Viewport = None
        self.viewport_size = viewport_size

        self.deferred_draws: List[DeferredDraw] = []

        self.create_buffers()
        self.bind_group: SceneBindGroup = None

    def _create(self):
        super()._create()
        self.create_bind_group()

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self.update_matrix()

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self.update_matrix()

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport):
        self._viewport = viewport
        if viewport is not None:
            self.on_viewport_size(viewport.size)
            viewport.add_listener(self)

    def on_viewport_size(self, size: glm.ivec2):
        self.viewport_size = glm.vec2(size.x, size.y)
        logger.debug(f"Camera3D: on_viewport_size: {size}")
        self.update_matrix()
        self.create_bind_group() # create a new bind group with the updated viewport

    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(CameraUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_group(self):
        self.bind_group = SceneBindGroup(
            self.uniform_buffer,
            self.uniform_buffer_size,
            self.viewport.uniform_buffer,
            self.viewport.uniform_buffer_size,
            self.viewport.snapshot_texture_view,
            self.viewport.snapshot_sampler,
        )

    '''
    def create_bind_group(self):
        camera_bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.uniform_buffer,
                size=self.uniform_buffer_size,
            ),
        ]

        camera_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Camera Bind Group",
            layout=CameraProgram3D().camera_bind_group_layout,
            entries=camera_bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(camera_bind_group_desc)
    '''

    def look_at(self, target: glm.vec3):
        self.view_matrix = glm.lookAt(self.position, target, self.up)

    def update_camera_vectors(self):
        # Update front, right, and up vectors using the orientation quaternion
        self.front = self.orientation * glm.vec3(0.0, 0.0, -1.0)
        self.right = self.orientation * glm.vec3(1.0, 0.0, 0.0)
        self.up = self.orientation * glm.vec3(0.0, 1.0, 0.0)

    def update_matrix(self):
        super().update_matrix()
        self.update_camera_vectors()
        size = self.viewport_size
        aspect = float(size.x) / float(size.y)
        fovy = glm.radians(60.0)
        self.projection_matrix = glm.perspective(fovy, aspect, self.near, self.far)

        self.update_gpu()

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.view_matrix)
        camera_uniform.position = cast_vec3(self.position)
        # logger.debug(f"camera_uniform.position: {camera_uniform.position.x}, {camera_uniform.position.y}, {camera_uniform.position.z}")

        self.device.queue.write_buffer(self.uniform_buffer, 0, camera_uniform)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        #pass_enc.set_bind_group(0, self.bind_group)
        self.bind_group.bind(pass_enc)

    def defer_draw(self, node: Node3D, callback: DrawCallback):
        self.deferred_draws.append(DeferredDraw(node, callback))

    def depth_of(self, node: Node3D) -> float:
        return glm.distance(self.position, node.position)

    def flush_deferred(self, renderer: "Renderer3D"):
        # sort by depth
        self.deferred_draws.sort(
            key=lambda d: self.depth_of(d.node),
            reverse=True,
        )
        for d in self.deferred_draws:
            #logger.debug(f"Camera3D: flushing deferred draw for {d.node}")
            d.callback()
        self.deferred_draws.clear()
