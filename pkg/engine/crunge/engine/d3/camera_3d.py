# camera_3d.py
from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu

from ..viewport import Viewport
from ..uniforms import cast_vec3, cast_matrix4
from ..binding import SceneBindGroup

from .node_3d import Node3D
from .uniforms_3d import CameraUniform
from .program_3d import Program3D


@klass.singleton
class CameraProgram3D(Program3D):
    pass


class Camera3D(Node3D):
    def __init__(
        self,
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
        self.viewport_size = glm.vec2(0, 0)

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
        if value == self._near:
            return
        self._near = value
        self._update_projection()
        self.update_gpu()

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        if value == self._far:
            return
        self._far = value
        self._update_projection()
        self.update_gpu()

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport):
        self._viewport = viewport
        if viewport is not None:
            self.on_viewport_size(viewport.size)
            viewport.size_changed.connect(self.on_viewport_size)

    def on_viewport_size(self, size: glm.ivec2):
        self.viewport_size = glm.vec2(size.x, size.y)
        logger.debug(f"Camera3D: on_viewport_size: {size}")
        self._update_projection()
        self.update_gpu()
        self.create_bind_group()

    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix

    def create_buffers(self):
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

    def look_at(self, target: glm.vec3):
        self.view_matrix = glm.lookAt(self.global_position, target, self.up)
        self.update_gpu()

    def update_camera_vectors(self):
        orientation = self.global_orientation
        self.front = orientation * glm.vec3(0.0, 0.0, -1.0)
        self.right = orientation * glm.vec3(1.0, 0.0, 0.0)
        self.up = orientation * glm.vec3(0.0, 1.0, 0.0)

    def on_transform(self):
        self.update_camera_vectors()
        self.update_gpu()
        super().on_transform()

    def _update_projection(self):
        size = self.viewport_size
        if size.y == 0:
            return
        aspect = float(size.x) / float(size.y)
        fovy = glm.radians(60.0)
        self.projection_matrix = glm.perspective(fovy, aspect, self.near, self.far)

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.view_matrix)
        camera_uniform.position = cast_vec3(self.global_position)

        self.device.queue.write_buffer(self.uniform_buffer, 0, camera_uniform)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)

    def depth_of(self, node: Node3D) -> float:
        return glm.distance(self.global_position, node.global_position)