from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from ..math import Size2, Size2i, Vector3,Point3
from .node_3d import Node3D
from .uniforms_3d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    LightUniform,
)

class Camera3D(Node3D):
    def __init__(
        self,
        size=Size2i(),
        position=Point3(0.0, 0.0, 4.0),
        up=Vector3(0.0, 1.0, 0.0),
    ):
        super().__init__(position)
        #self.position = position
        #self.orientation = glm.quat()
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)
        self.size = size
        self.zoom = 45.0

        self.up = up
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self.update_camera_vectors()

        #self.create_buffers()
        #self.create_bind_groups()

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size: glm.ivec2):
        self._size = size
        aspect = float(size.x) / float(size.y)
        fovy = glm.radians(60.0)
        self.projection_matrix = glm.perspective(fovy, aspect, .1, 100.0)

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

    def create_bind_groups(self):
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(camera_bgl_entries), entries=camera_bgl_entries
        )
        camera_bgl = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {camera_bgl}")

        camera_bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.uniform_buffer,
                size=self.uniform_buffer_size,
            ),
        ]

        camera_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Camera bind group",
            layout=camera_bgl,
            entry_count=len(camera_bindgroup_entries),
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

    def on_viewport_size(self, size: Size2i):
        self.size = Size2(size.x, size.y)

    def on_size(self) -> None:
        super().on_size()
        self.update_matrix()

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.model_matrix.data = cast_matrix4(model_matrix)
        camera_uniform.transform_matrix.data = cast_matrix4(transform_matrix)
        #camera_uniform.normal_matrix.data = cast_matrix3(normal_matrix)
        camera_uniform.normal_matrix.data = cast_matrix4(normal_matrix)

        # camera_uniform.position.x = camera.position.x
        # camera_uniform.position.y = camera.position.y
        # camera_uniform.position.z = camera.position.z
        camera_uniform.position = cast_vec3(camera.position)
        #logger.debug(f"camera_uniform.position: {camera_uniform.position.x}, {camera_uniform.position.y}, {camera_uniform.position.z}")

        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )
