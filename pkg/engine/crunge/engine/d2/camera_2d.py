import contextlib

import glm
from loguru import logger

from crunge import wgpu
from crunge.core import klass
from crunge.core.signal import Signal, Pulse

from ..math import Bounds2, Rect2i
from ..viewport import Viewport
from ..easel import Easel
from ..camera_chip import CameraChip

from .renderer import Renderer2D
from .node_2d import Node2D
from .settings_2d import Settings2D
from .program_2d import Program2D


# Zoom is clamped here rather than rejected, so a drag slider bottoming out
# can't collapse the frustum to a point.
MIN_ZOOM = 0.01


@klass.singleton
class CameraProgram2D(Program2D):
    pass


class CameraChip2D(CameraChip["Camera2D"]):
    def eye_of(self, node: "Camera2D") -> glm.vec3:
        position = node.global_position
        return glm.vec3(position.x, position.y, 0.0)


class Camera2D(Node2D):
    """Orthographic 2D camera.

    `zoom` is magnification: 2.0 shows everything twice as large, 0.5 half as
    large. The visible world width is `viewport_width / ppu / zoom`.

    A camera with a leader follows the leader's position (scaled by
    parallax_factor about parallax_origin) and copies its zoom.
    """

    def __init__(
        self,
        position: glm.vec2 = None,
        zoom: float = 1.0,
        leader: "Camera2D" = None,
        parallax_factor: glm.vec2 = None,
        parallax_origin: glm.vec2 = None,
        ppu: float = None,
    ):
        # Vector defaults are built per instance: glm vectors are mutable, so a
        # shared default would be shared state between every camera.
        super().__init__(position if position is not None else glm.vec2(0.0, 0.0))

        self._zoom = max(zoom, MIN_ZOOM)
        if ppu is not None:
            self.ppu = ppu
        elif leader is not None:
            self.ppu = leader.ppu
        else:
            self.ppu = Settings2D().ppu

        self.parallax_factor = (
            parallax_factor if parallax_factor is not None else glm.vec2(1.0, 1.0)
        )
        self.parallax_origin = (
            parallax_origin if parallax_origin is not None else glm.vec2(0.0, 0.0)
        )

        self.position_changed: Signal[glm.vec2] = Signal()
        self.zoom_changed: Signal[float] = Signal()

        # Payload-free: the chip reads current state off the node when it
        # flushes, and there is one subscriber.
        self.camera_changed = Pulse()
        self.binding_changed = Pulse()

        self.projection_matrix = glm.mat4(1.0)
        self.view_matrix = glm.mat4(1.0)
        self.frustum: Bounds2 | None = None

        self._viewport: Viewport | None = None
        self.viewport_size = glm.vec2(0.0, 0.0)

        self._leader: "Camera2D | None" = None
        self.leader = leader

    # -- lifecycle ---------------------------------------------------------

    def _seat(self) -> None:
        super()._seat()
        if not self.has_chip(CameraChip2D):
            self.add_chip(CameraChip2D())

    def _destroy(self):
        # Under gc.disable(), these connections are what keep a dead camera
        # reachable — and receiving callbacks — from a live leader or viewport.
        # Disconnect directly rather than through the viewport setter, which
        # would emit binding_changed mid-teardown.
        if self._viewport is not None:
            self._viewport.rect_changed.disconnect(self.on_viewport_rect)
            self._viewport = None
        self.leader = None
        super()._destroy()

    # -- chip forwarding ---------------------------------------------------

    @property
    def chip(self) -> CameraChip2D | None:
        return self.get_chip(CameraChip2D)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.require_chip(CameraChip2D).bind(pass_enc)

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

    # -- viewport ----------------------------------------------------------

    @property
    def viewport(self) -> Viewport | None:
        return self._viewport

    @viewport.setter
    def viewport(self, viewport: Viewport | None):
        if self._viewport is not None:
            self._viewport.rect_changed.disconnect(self.on_viewport_rect)
        self._viewport = viewport
        if viewport is not None:
            viewport.rect_changed.connect(self.on_viewport_rect)
            self.on_viewport_rect(viewport.global_rect)
        else:
            self.binding_changed.emit()

    @property
    def easel(self) -> Easel:
        return self.viewport.easel

    def on_viewport_rect(self, rect: Rect2i):
        logger.debug(f"Camera2D: on_viewport_rect: {rect}")
        self.viewport_size = glm.vec2(rect.width, rect.height)
        self._update_camera_matrices()
        # Rebuilding the bind group here could run before the buffer existed
        # and mid-frame, so the chip does it on its own schedule.
        self.binding_changed.emit()

    # -- zoom --------------------------------------------------------------

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, value: float):
        value = max(value, MIN_ZOOM)
        if value == self._zoom:
            return
        self._zoom = value
        self._update_camera_matrices()
        self.zoom_changed.emit(value)

    @property
    def zoom_pct(self) -> float:
        return self._zoom * 100.0

    @zoom_pct.setter
    def zoom_pct(self, pct: float):
        self.zoom = pct / 100.0

    # -- leader ------------------------------------------------------------

    @property
    def leader(self) -> "Camera2D | None":
        return self._leader

    @leader.setter
    def leader(self, value: "Camera2D | None"):
        if value is self._leader:
            return
        if self._leader is not None:
            self._leader.position_changed.disconnect(self.on_leader_position)
            self._leader.zoom_changed.disconnect(self.on_leader_zoom)
        self._leader = value
        if value is not None:
            value.position_changed.connect(self.on_leader_position)
            value.zoom_changed.connect(self.on_leader_zoom)
            # Sync through the setters so matrices update and signals fire.
            # Assigning _zoom directly here used to make on_leader_zoom a no-op.
            self.on_leader_position(value.position)
            self.on_leader_zoom(value.zoom)

    def on_leader_position(self, position: glm.vec2):
        self.position = (
            self.parallax_origin
            + (position - self.parallax_origin) * self.parallax_factor
        )

    def on_leader_zoom(self, zoom: float):
        self.zoom = zoom

    # -- transform ---------------------------------------------------------

    def on_transform(self):
        self._update_camera_matrices()
        self.position_changed.emit(self.position)
        super().on_transform()
        # transform_changed is emitted by SceneNode right after this hook,
        # so the chip marks itself; no explicit camera_changed needed.

    def _update_camera_matrices(self):
        # With no viewport yet, the frustum would have zero extent and
        # glm.ortho would produce an infinite matrix. Wait for on_viewport_rect.
        if self.viewport_size.x <= 0 or self.viewport_size.y <= 0:
            self.frustum = None
            return

        view_width = self.viewport_size.x / self.ppu / self._zoom
        view_height = self.viewport_size.y / self.ppu / self._zoom

        center = self.global_position
        left = center.x - view_width / 2
        right = center.x + view_width / 2
        bottom = center.y - view_height / 2
        top = center.y + view_height / 2

        self.frustum = Bounds2(left, bottom, right, top)
        self.projection_matrix = glm.ortho(left, right, bottom, top, -1, 1)
        self.camera_changed.emit()

    # -- screen <-> world --------------------------------------------------

    def _can_map(self) -> bool:
        frustum = self.frustum
        return (
            self.viewport_size.x > 0
            and self.viewport_size.y > 0
            and frustum is not None
            and frustum.is_finite()
            and frustum.width > 0
            and frustum.height > 0
        )

    def unproject(self, screen: glm.vec2) -> glm.vec2:
        """Viewport pixels (y down) -> world units (y up)."""
        if not self._can_map():
            return glm.vec2(0.0, 0.0)

        frustum = self.frustum
        x_ndc = (2.0 * screen.x / self.viewport_size.x) - 1.0
        y_ndc = 1.0 - (2.0 * screen.y / self.viewport_size.y)

        return frustum.center + glm.vec2(
            x_ndc * frustum.width / 2.0,
            y_ndc * frustum.height / 2.0,
        )

    def project(self, world: glm.vec2) -> glm.vec2:
        """World units (y up) -> viewport pixels (y down). Inverse of unproject."""
        if not self._can_map():
            return glm.vec2(0.0, 0.0)

        frustum = self.frustum
        offset = world - frustum.center
        x_ndc = offset.x / (frustum.width / 2.0)
        y_ndc = offset.y / (frustum.height / 2.0)

        return glm.vec2(
            (x_ndc + 1.0) * self.viewport_size.x / 2.0,
            (1.0 - y_ndc) * self.viewport_size.y / 2.0,
        )