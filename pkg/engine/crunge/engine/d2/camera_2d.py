from ctypes import sizeof

import glm

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..math import Bounds2
from ..uniforms import cast_matrix4, cast_vec3, cast_vec2
from ..viewport import Viewport, ViewportListener

from .node_2d import Node2D
from .uniforms_2d import CameraUniform

from .program_2d import Program2D
from .bindings import CameraBindGroup


@klass.singleton
class CameraProgram2D(Program2D):
    pass


class Camera2D(Node2D, ViewportListener):
    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 2),
        viewport_size=glm.vec2(1024, 768),
        zoom=1.0,
    ):
        self._zoom = zoom
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.projection_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)

        self.frustrum: Bounds2 = None

        self._viewport: Viewport = None
        self.viewport_size = viewport_size

        self.create_buffers()
        self.create_bind_group()

        super().__init__(position)

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport):
        self._viewport = viewport
        if viewport is not None:
            self.on_viewport_size(viewport.size)
            viewport.add_listener(self)

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

    def create_bind_group(self):
        self.bind_group = CameraBindGroup(
            self.uniform_buffer,
            self.uniform_buffer_size,
        )

    def on_viewport_size(self, size: glm.ivec2):
        self.viewport_size = glm.vec2(size.x, size.y)
        logger.debug(f"Camera2D: on_viewport_size: {size}")
        self.update_matrix()

    def update_matrix(self):
        super().update_matrix()
        viewport_size = self.viewport_size
        viewport_width = viewport_size.x
        viewport_height = viewport_size.y
        ortho_left = self.x - (viewport_width * self.zoom) / 2
        ortho_right = self.x + (viewport_width * self.zoom) / 2
        ortho_bottom = self.y - (viewport_height * self.zoom) / 2
        ortho_top = self.y + (viewport_height * self.zoom) / 2

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
        #camera_uniform.viewport = cast_vec2(self.viewport_size)
        camera_uniform.position = cast_vec3(
            glm.vec3(self.position.x, self.position.y, 0)
        )

        self.device.queue.write_buffer(self.uniform_buffer, 0, camera_uniform)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)

    def unproject(self, mouse_vec: glm.vec2):
        mx = mouse_vec.x
        my = mouse_vec.y
        # Get viewport dimensions
        viewport = self.viewport
        viewportWidth = viewport.width
        viewPortHeight = viewport.height

        frustrum = self.frustrum
        glOrthoWidth = frustrum.width
        glOrthoHeight = frustrum.height

        # Convert mouse coordinates to NDC
        x_ndc = (2.0 * mx / viewportWidth) - 1.0
        y_ndc = (2.0 * my / viewPortHeight) - 1.0
        y_ndc = -y_ndc  # Flip Y for WebGPU's coordinate system

        # Convert NDC to world coordinates using the adjusted projection size
        x_world = x_ndc * (glOrthoWidth / 2.0)
        y_world = y_ndc * (glOrthoHeight / 2.0)

        # Adjust for camera position
        x_world += self.x
        y_world += self.y
        return glm.vec2(x_world, y_world)
