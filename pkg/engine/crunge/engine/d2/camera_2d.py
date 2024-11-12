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

from ..math import Bounds2
from ..math.rect import Rect2
from ..uniforms import cast_matrix4, cast_vec3
from ..viewport import Viewport

from .node_2d import Node2D
from .uniforms_2d import (
    CameraUniform,
)
from .program_2d import Program2D

@klass.singleton
class CameraProgram2D(Program2D):
    pass

class Camera2D(Node2D):
    def __init__(self, position=glm.vec3(0.0, 0.0, 2), size=glm.vec2(1.0), zoom=1.0):
        self._zoom = zoom
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.projection_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)

        self.frustrum: Bounds2 = None
        #self.projection = Rect2()

        self._viewport: Viewport = None
        self.viewport_size_subscription: Subscription[glm.ivec2] = None

        self.create_buffers()
        self.create_bind_groups()

        super().__init__(position, size)

    '''
    @property
    def frustrum(self) -> Bounds2:
        half_width = (self.width / 2) * self.zoom
        half_height = (self.height / 2) * self.zoom
        min_x = self.position.x - half_width
        max_x = self.position.x + half_width
        min_y = self.position.y - half_height
        max_y = self.position.y + half_height
        bounds = Bounds2(glm.vec2(min_x, min_y), glm.vec2(max_x, max_y))
        logger.debug(f"Camera frustrum: {bounds}")
        return bounds
    '''

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

    def on_viewport_size(self, size: glm.ivec2):
        self.size = glm.vec2(size.x, size.y)

    def on_size(self) -> None:
        super().on_size()
        self.update_matrix()

    def update_matrix(self):
        super().update_matrix()
        ortho_left = self.x - (self.width * self.zoom) / 2
        ortho_right = self.x + (self.width * self.zoom) / 2
        ortho_bottom = self.y - (self.height * self.zoom) / 2
        ortho_top = self.y + (self.height * self.zoom) / 2

        '''
        self.projection = Rect2(
            ortho_left, ortho_bottom, ortho_right - ortho_left, ortho_top - ortho_bottom
        )
        '''
        self.frustrum = Bounds2(ortho_left, ortho_bottom, ortho_right, ortho_top)

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
        camera_uniform.position = cast_vec3(glm.vec3(self.position.x, self.position.y, 0))

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.uniform_buffer_size,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(0, self.bind_group)
