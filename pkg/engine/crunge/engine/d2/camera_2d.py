import contextlib
from ctypes import sizeof

import glm

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from ..signal import Signal
from ..math import Bounds2, Rect2i
from ..uniforms import cast_matrix4, cast_vec3
from ..viewport import Viewport
from ..easel import Easel
from ..binding import SceneBindGroup

from .renderer import Renderer2D
from .node_2d import Node2D
from .uniforms_2d import CameraUniform
from .settings_2d import Settings2D

from .program_2d import Program2D


@klass.singleton
class CameraProgram2D(Program2D):
    pass


class Camera2D(Node2D):
    def __init__(
        self,
        position=glm.vec2(0.0, 0.0),
        zoom=1.0,
        leader: "Camera2D" = None,
        parallax_factor=glm.vec2(1.0, 1.0),
        parallax_origin=glm.vec2(0.0, 0.0),
        ppu: float = None,
    ):
        super().__init__(position)

        self._zoom = zoom
        self.ppu = (
            ppu
            if ppu is not None
            else (leader.ppu if leader is not None else Settings2D().ppu)
        )

        self._leader: "Camera2D" = None

        self.position_changed: Signal[glm.vec2] = Signal()
        self.zoom_changed: Signal[float] = Signal()

        self.parallax_factor = parallax_factor
        self.parallax_origin = parallax_origin
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.projection_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)

        self.frustum: Bounds2 = None

        self._viewport: Viewport = None
        self.viewport_size = glm.vec2(0, 0)

        self.create_buffers()
        self.bind_group: SceneBindGroup = None

        self.leader = leader

    def _create(self):
        super()._create()
        self.create_bind_group()

    @contextlib.contextmanager
    def use(self):
        current_renderer = Renderer2D.get_current()
        prev_camera = current_renderer.camera_2d
        current_renderer.camera_2d = self
        self.bind(current_renderer.pass_enc)
        yield self
        current_renderer.camera_2d = prev_camera
        prev_camera.bind(current_renderer.pass_enc)

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport):
        if self._viewport is not None:
            self._viewport.rect_changed.disconnect(self.on_viewport_rect)
        self._viewport = viewport
        if viewport is not None:
            viewport.rect_changed.connect(self.on_viewport_rect)
            self.on_viewport_rect(viewport.global_rect)

    def on_viewport_rect(self, rect: Rect2i):
        logger.debug(f"Camera2D: on_viewport_rect: {rect}")

        self.viewport_size = rect.size
        self._update_camera_matrices()
        self.create_bind_group()

    @property
    def easel(self) -> Easel:
        return self.viewport.easel

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        if value == self._zoom:
            return
        self._zoom = value
        self._update_camera_matrices()
        self.zoom_changed.emit(value)

    @property
    def leader(self):
        return self._leader

    @leader.setter
    def leader(self, value: "Camera2D"):
        if value == self._leader:
            return
        if self._leader is not None:
            self._leader.position_changed.disconnect(self.on_leader_position)
            self._leader.zoom_changed.disconnect(self.on_leader_zoom)
        self._leader = value
        if value is not None:
            self._zoom = value.zoom
            value.position_changed.connect(self.on_leader_position)
            value.zoom_changed.connect(self.on_leader_zoom)
            self.on_leader_position(value.position)
            self.on_leader_zoom(value.zoom)

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
            self.easel.snapshot_texture_view,
            self.easel.snapshot_sampler,
        )

    def on_leader_position(self, position: glm.vec2):
        self.position = (
            self.parallax_origin
            + (position - self.parallax_origin) * self.parallax_factor
        )

    def on_leader_zoom(self, zoom: float):
        logger.debug(f"Camera2D: on_leader_zoom: {zoom}")
        self.zoom = zoom

    def on_transform(self):
        self._update_camera_matrices()
        self.position_changed.emit(self.position)
        super().on_transform()

    def _update_camera_matrices(self):
        view_width = (self.viewport_size.x / self.ppu) * self.zoom
        view_height = (self.viewport_size.y / self.ppu) * self.zoom

        ortho_left = self.x - view_width / 2
        ortho_right = self.x + view_width / 2
        ortho_bottom = self.y - view_height / 2
        ortho_top = self.y + view_height / 2

        self.frustum = Bounds2(ortho_left, ortho_bottom, ortho_right, ortho_top)

        self.projection_matrix = glm.ortho(
            ortho_left, ortho_right, ortho_bottom, ortho_top, -1, 1
        )
        self.update_gpu()

    def update_gpu(self):
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(self.projection_matrix)
        camera_uniform.view.data = cast_matrix4(self.view_matrix)
        position = self.global_position
        camera_uniform.position = cast_vec3(glm.vec3(position.x, position.y, 0))

        self.device.queue.write_buffer(self.uniform_buffer, 0, camera_uniform)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)

    def unproject(self, mouse_vec: glm.vec2):
        viewport_width = self.viewport_size.x
        viewport_height = self.viewport_size.y

        mx = mouse_vec.x
        my = mouse_vec.y

        frustum = self.frustum
        frustum_width = frustum.width
        frustum_height = frustum.height

        x_ndc = (2.0 * mx / viewport_width) - 1.0
        y_ndc = (2.0 * my / viewport_height) - 1.0
        y_ndc = -y_ndc

        x_world = x_ndc * (frustum_width / 2.0)
        y_world = y_ndc * (frustum_height / 2.0)

        x_world += self.x
        y_world += self.y

        return glm.vec2(x_world, y_world)
