# camera_3d.py
from ctypes import sizeof

from crunge.engine.math.rect import Rect2i
from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu

from ..viewport import Viewport
from ..easel import Easel
#from ..binding import SceneBindGroup
from crunge.core.signal import Pulse
from ..camera_chip import CameraChip

from .node_3d import Node3D
from .program_3d import Program3D


@klass.singleton
class CameraProgram3D(Program3D):
    pass




class CameraChip3D(CameraChip["Camera3D"]):
    pass

class Camera3D(Node3D):
    def __init__(
        self,
        position: glm.vec3 = None,
        up: glm.vec3 = None,
        near: float = 0.1,
        far: float = 100.0,
    ):
        # None sentinels: glm.vec3 defaults are shared mutable instances
        # across every camera ever constructed.
        super().__init__(glm.vec3(0.0, 0.0, 4.0) if position is None else position)
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)
        self.zoom = 45.0

        self.up = glm.vec3(0.0, 1.0, 0.0) if up is None else glm.vec3(up)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self._near = near
        self._far = far

        self._viewport: Viewport = None
        self.viewport_size = glm.vec2(0, 0)

        # Payload-free: the chip reads current state off the node when it
        # flushes, and there is one subscriber.
        self.camera_changed = Pulse()
        self.binding_changed = Pulse()

    def _seat(self) -> None:
        super()._seat()
        if not self.has(CameraChip3D):
            self.add(CameraChip3D())

    # -- chip forwarding ---------------------------------------------------

    @property
    def chip(self) -> CameraChip3D | None:
        return self.get(CameraChip3D)

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
        self.require(CameraChip3D).bind(pass_enc)

    # -- properties --------------------------------------------------------

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        if value == self._near:
            return
        self._near = value
        self._update_projection()
        self.camera_changed.emit()

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        if value == self._far:
            return
        self._far = value
        self._update_projection()
        self.camera_changed.emit()

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
        self.viewport_size = glm.vec2(rect.width, rect.height)
        logger.debug(f"Camera3D: on_viewport_rect: {rect}")
        self._update_projection()
        # Was rebuilding the bind group inline, which could run before the
        # buffer existed and during a frame.
        self.binding_changed.emit()

    @property
    def easel(self) -> Easel:
        return self.viewport.easel

    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix

    def look_at(self, target: glm.vec3):
        self.view_matrix = glm.lookAt(self.global_position, target, self.up)
        self.camera_changed.emit()

    def update_camera_vectors(self):
        orientation = self.global_orientation
        self.front = orientation * glm.vec3(0.0, 0.0, -1.0)
        self.right = orientation * glm.vec3(1.0, 0.0, 0.0)
        self.up = orientation * glm.vec3(0.0, 1.0, 0.0)

    def on_transform(self):
        self.update_camera_vectors()
        super().on_transform()
        # transform_changed is emitted by SceneNode right after this hook,
        # so the chip marks itself; no explicit camera_changed needed.

    def _update_projection(self):
        size = self.viewport_size
        if size.y == 0:
            return
        aspect = float(size.x) / float(size.y)
        fovy = glm.radians(60.0)
        self.projection_matrix = glm.perspective(fovy, aspect, self.near, self.far)

    def depth_of(self, node: Node3D) -> float:
        return glm.distance(self.global_position, node.global_position)