from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge.core.event_source import Subscription

from crunge import wgpu

from ..viewport import Viewport, ViewportListener
from ..uniforms import cast_vec3, cast_matrix4

from .node_3d import Node3D
from .uniforms_3d import (
    CameraUniform,
)
from .program_3d import Program3D


@klass.singleton
class CameraProgram3D(Program3D):
    pass


class Camera3D(Node3D, ViewportListener):
    def __init__(
        self,
        size=glm.ivec2(),
        position=glm.vec3(0.0, 0.0, 4.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        near=0.1,
        far=100.0,
    ):
        #super().__init__(position)
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)
        self._size = size
        self.zoom = 45.0

        self.up = up
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self._near = near
        self._far = far

        self._viewport: Viewport = None
        self.viewport_size_subscription: Subscription[glm.ivec2] = None

        self.create_buffers()
        self.create_bind_group()

        super().__init__(position)

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
            '''
            self.viewport_size_subscription = viewport.size_events.subscribe(
                self.on_viewport_size
            )
            '''
            viewport.add_listener(self)

    def on_viewport_size(self, size: glm.ivec2):
        self.size = size

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size: glm.ivec2):
        self._size = size
        self.update_matrix()

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

    def look_at(self, target: glm.vec3):
        self.view_matrix = glm.lookAt(self.position, target, self.up)

    def update_camera_vectors(self):
        # Update front, right, and up vectors using the orientation quaternion
        self.front = self.orientation * glm.vec3(0.0, 0.0, -1.0)
        self.right = self.orientation * glm.vec3(1.0, 0.0, 0.0)
        self.up = self.orientation * glm.vec3(0.0, 1.0, 0.0)

    def on_viewport_size(self, size: glm.ivec2):
        self.size = glm.vec2(size.x, size.y)

    def on_size(self) -> None:
        super().on_size()
        self.update_matrix()

    def update_matrix(self):
        super().update_matrix()
        self.update_camera_vectors()
        size = self.size
        aspect = float(size.x) / float(size.y)
        fovy = glm.radians(60.0)
        self.projection_matrix = glm.perspective(fovy, aspect, self.near, self.far)

        self.update_gpu()

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.view_matrix)
        camera_uniform.position = cast_vec3(self.position)
        #logger.debug(f"camera_uniform.position: {camera_uniform.position.x}, {camera_uniform.position.y}, {camera_uniform.position.z}")

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            camera_uniform
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(0, self.bind_group)
