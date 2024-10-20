from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

import glm

from loguru import logger

from crunge import wgpu
from crunge.core import as_capsule
from crunge.core import klass
from crunge.core.event_source import Subscription

from ..math import Point3, Size2, Size2i
from ..math.rect import Rect2
from ..viewport import Viewport

from .node_2d import Node2D
from .uniforms_2d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
)
from .program_2d import Program2D

@klass.singleton
class CameraProgram2D(Program2D):
    pass

class Camera2D(Node2D):
    def __init__(self, position=Point3(0.0, 0.0, 2), size=Size2(1.0)):
        self._zoom = 1.0
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0
        self.view_matrix = glm.mat4(1.0)
        self.projection = Rect2()

        self._viewport: Viewport = None
        self.viewport_size_subscription: Subscription[Size2i] = None

        self.create_buffers()
        self.create_bind_groups()

        super().__init__(position, size)

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport):
        self._viewport = viewport
        if viewport is not None:
            self.viewport_size_subscription = viewport.size_events.subscribe(
                self.on_viewport_size
            )

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        self._zoom = value
        self.update_matrix()

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(CameraUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        camera_bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.uniform_buffer,
                size=self.uniform_buffer_size,
            ),
        ]

        camera_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Camera bind group",
            #layout=camera_bgl,
            layout=CameraProgram2D().camera_bind_group_layout,
            entry_count=len(camera_bindgroup_entries),
            entries=camera_bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(camera_bind_group_desc)

    def on_viewport_size(self, size: Size2i):
        self.size = Size2(size.x, size.y)

    def on_size(self) -> None:
        super().on_size()
        self.update_matrix()

    def update_matrix(self):
        super().update_matrix()
        ortho_left = self.x - (self.width * self.zoom) / 2
        ortho_right = self.x + (self.width * self.zoom) / 2
        ortho_bottom = self.y - (self.height * self.zoom) / 2
        ortho_top = self.y + (self.height * self.zoom) / 2

        self.projection = Rect2(
            ortho_left, ortho_bottom, ortho_right - ortho_left, ortho_top - ortho_bottom
        )

        ortho_near = -1  # Near clipping plane
        ortho_far = 1  # Far clipping plane

        self.projection_matrix = glm.ortho(
            ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far
        )
        self.update_gpu()

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.view_matrix)
        camera_uniform.position = cast_vec3(Point3(self.position.x, self.position.y, 0))

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.uniform_buffer_size,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(0, self.bind_group)
