import contextlib

import glm

from loguru import logger

from crunge import wgpu
from crunge.core import klass

from crunge.core.signal import Signal, Pulse
from ..math import Bounds2, Rect2i
from ..viewport import Viewport
from ..easel import Easel
#from ..binding import SceneBindGroup
from ..camera_chip import CameraChip

from .renderer import Renderer2D
from .node_2d import Node2D
from .settings_2d import Settings2D

from .program_2d import Program2D


@klass.singleton
class CameraProgram2D(Program2D):
    pass


class CameraChip2D(CameraChip["Camera2D"]):
    def eye_of(self, node: "Camera2D") -> glm.vec3:
        position = node.global_position
        return glm.vec3(position.x, position.y, 0.0)


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

        # Payload-free: the chip reads current state off the node when it
        # flushes, and there is one subscriber.
        self.camera_changed = Pulse()
        self.binding_changed = Pulse()

        self.parallax_factor = parallax_factor
        self.parallax_origin = parallax_origin

        self.projection_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)

        self.frustum: Bounds2 = None

        self._viewport: Viewport = None
        self.viewport_size = glm.vec2(0, 0)

        self.leader = leader

    def _seat(self) -> None:
        super()._seat()
        if not self.has(CameraChip2D):
            self.add(CameraChip2D())

    # -- chip forwarding ---------------------------------------------------

    @property
    def chip(self) -> CameraChip2D | None:
        return self.get(CameraChip2D)

    '''
    @property
    def uniform_buffer(self) -> wgpu.Buffer:
        chip = self.chip
        return chip.uniform_buffer if chip is not None else None

    @property
    def uniform_buffer_size(self) -> int:
        chip = self.chip
        return chip.uniform_buffer_size if chip is not None else 0

    @property
    def bind_group(self) -> SceneBindGroup:
        chip = self.chip
        return chip.bind_group if chip is not None else None
    '''

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.require(CameraChip2D).bind(pass_enc)

    # -- use ---------------------------------------------------------------
    @contextlib.contextmanager
    def use(self):
        renderer = Renderer2D.get_current()
        if renderer is None:
            raise RuntimeError("Camera2D.use() requires a current renderer.")
        prev_camera = renderer.camera_2d
        renderer.camera_2d = self
        self.bind(renderer.pass_enc)
        try:
            yield self
        finally:
            renderer.camera_2d = prev_camera
            if prev_camera is not None:
                prev_camera.bind(renderer.pass_enc)
    '''
    @contextlib.contextmanager
    def use(self):
        current_renderer = Renderer2D.get_current()
        prev_camera = current_renderer.camera_2d
        current_renderer.camera_2d = self
        self.bind(current_renderer.pass_enc)
        yield self
        current_renderer.camera_2d = prev_camera
        prev_camera.bind(current_renderer.pass_enc)
    '''
    # -- properties --------------------------------------------------------

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
        else:
            self.binding_changed.emit()

    def on_viewport_rect(self, rect: Rect2i):
        logger.debug(f"Camera2D: on_viewport_rect: {rect}")

        self.viewport_size = glm.vec2(rect.width, rect.height)
        self._update_camera_matrices()
        # Was rebuilding the bind group inline, which could run before the
        # buffer existed and during a frame.
        self.binding_changed.emit()

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

    # -- transform ---------------------------------------------------------

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
        # transform_changed is emitted by SceneNode right after this hook,
        # so the chip marks itself; no explicit camera_changed needed.

    def _update_camera_matrices(self):
        view_width = (self.viewport_size.x / self.ppu) * self.zoom
        view_height = (self.viewport_size.y / self.ppu) * self.zoom

        center = self.global_position
        ortho_left = center.x - view_width / 2
        ortho_right = center.x + view_width / 2
        ortho_bottom = center.y - view_height / 2
        ortho_top = center.y + view_height / 2

        self.frustum = Bounds2(ortho_left, ortho_bottom, ortho_right, ortho_top)

        self.projection_matrix = glm.ortho(
            ortho_left, ortho_right, ortho_bottom, ortho_top, -1, 1
        )
        self.camera_changed.emit()

    '''
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
        self.camera_changed.emit()
    '''

    def unproject(self, mouse_vec: glm.vec2):
        viewport_width = self.viewport_size.x
        viewport_height = self.viewport_size.y
        if viewport_width == 0 or viewport_height == 0:
            return glm.vec2(0.0, 0.0)

        frustum = self.frustum
        if frustum is None or not frustum.is_finite():
            return glm.vec2(0.0, 0.0)

        x_ndc = (2.0 * mouse_vec.x / viewport_width) - 1.0
        y_ndc = -((2.0 * mouse_vec.y / viewport_height) - 1.0)

        return frustum.center + glm.vec2(
            x_ndc * frustum.width / 2.0,
            y_ndc * frustum.height / 2.0,
        )

    '''
    def unproject(self, mouse_vec: glm.vec2):
        viewport_width = self.viewport_size.x
        viewport_height = self.viewport_size.y
        if viewport_width == 0 or viewport_height == 0:
            return glm.vec2(0.0, 0.0)

        frustum = self.frustum

        x_ndc = (2.0 * mouse_vec.x / viewport_width) - 1.0
        y_ndc = -((2.0 * mouse_vec.y / viewport_height) - 1.0)

        center = self.global_position
        x_world = center.x + x_ndc * (frustum.width / 2.0)
        y_world = center.y + y_ndc * (frustum.height / 2.0)

        return glm.vec2(x_world, y_world)
    '''

    '''
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
    '''