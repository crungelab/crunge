# camera_3d.py
from ctypes import sizeof

from crunge.engine.math.rect import Rect2i
from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu

from ..viewport import Viewport
from ..easel import Easel
from ..uniforms import cast_vec3, cast_matrix4
from ..binding import SceneBindGroup
from ..signal import Pulse
from ..chip import Chip

from .node_3d import Node3D
from .uniforms_3d import CameraUniform
from .program_3d import Program3D


@klass.singleton
class CameraProgram3D(Program3D):
    pass


class CameraChip(Chip["Camera3D"]):
    """Owns the camera's uniform buffer and scene bind group.

    Two dirt domains. The uniform is rewritten whenever the camera moves or
    its projection changes; the bind group is rebuilt only when what it
    references changes — the viewport or the easel's snapshot texture. The
    bind group also cannot be built until a viewport is assigned, which is
    why it retries rather than throwing.
    """

    def __init__(self) -> None:
        super().__init__()
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0
        self.bind_group: SceneBindGroup = None

    def _create(self) -> None:
        super()._create()
        self.uniform_buffer_size = sizeof(CameraUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    # -- listening ---------------------------------------------------------

    def listen(self) -> None:
        node = self.node
        node.transform_changed.connect(self.on_transform_changed)
        node.camera_changed.connect(self.mark_gpu)
        node.binding_changed.connect(self.on_binding_changed)

    def deafen(self) -> None:
        node = self._node
        if node is None:
            return
        node.transform_changed.disconnect(self.on_transform_changed)
        node.camera_changed.disconnect(self.mark_gpu)
        node.binding_changed.disconnect(self.on_binding_changed)

    def sync(self) -> None:
        self.mark_binding()
        self.mark_gpu()

    def on_transform_changed(self, node: "Camera3D") -> None:
        self.mark_gpu()

    def on_binding_changed(self) -> None:
        # The uniform goes with it: a viewport change moves the projection.
        self.mark_binding()
        self.mark_gpu()

    # -- deferred rebuild --------------------------------------------------

    def update(self, delta_time: float) -> None:
        self.flush()

    def _flush_binding(self) -> bool:
        if self.uniform_buffer is None:
            return False

        node = self.node
        viewport = node.viewport
        if viewport is None:
            return False  # no viewport assigned yet; retry
        easel = viewport.easel
        if easel is None:
            return False

        self.bind_group = SceneBindGroup(
            self.uniform_buffer,
            self.uniform_buffer_size,
            viewport.uniform_buffer,
            viewport.uniform_buffer_size,
            easel.snapshot_texture_view,
            easel.snapshot_sampler,
        )
        return True

    def _flush_gpu(self) -> bool:
        if self.uniform_buffer is None:
            return False

        node = self.node
        camera_uniform = CameraUniform()
        camera_uniform.projection.data = cast_matrix4(node.projection_matrix)
        camera_uniform.view.data = cast_matrix4(node.view_matrix)
        camera_uniform.position = cast_vec3(node.global_position)

        self.gfx.device.queue.write_buffer(self.uniform_buffer, 0, camera_uniform)
        return True

    # -- frame -------------------------------------------------------------
    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        node = self._node
        '''
        logger.debug(
            f"camera flush: pos={node.global_position} "
            f"proj[0][0]={node.projection_matrix[0][0]:.4f} "
            f"view[3]={node.view_matrix[3]}"
        )
        '''

        self.flush()
        if self.bind_group is None:
            raise RuntimeError(
                f"{self!r} has no bind group: "
                f"viewport={self._node.viewport if self._node else None} "
                f"buffer={self.uniform_buffer is not None}"
            )
        self.bind_group.bind(pass_enc)

    """
    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        if self.bind_group is None:
            raise RuntimeError(
                f"{self!r} has no bind group: viewport="
                f"{self._node.viewport if self._node else None}"
            )
        self.bind_group.bind(pass_enc)
    """

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
        if not self.has(CameraChip):
            self.add(CameraChip())

    # -- chip forwarding ---------------------------------------------------

    @property
    def chip(self) -> CameraChip | None:
        return self.get(CameraChip)

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

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.require(CameraChip).bind(pass_enc)

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