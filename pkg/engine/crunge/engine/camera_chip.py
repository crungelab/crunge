from ctypes import sizeof

import glm

from crunge import wgpu

from crunge.core.chip import Chip
from .binding import SceneBindGroup
from .gfx_access import GfxAccess
from .uniforms import cast_matrix4, cast_vec3, CameraUniform


class CameraChip[NodeT](GfxAccess, Chip[NodeT]):
    """Owns a camera's uniform buffer and scene bind group.

    Two dirt domains. The uniform is rewritten whenever the camera moves or
    its projection changes; the bind group is rebuilt only when what it
    references changes — the viewport or the easel's snapshot texture. The
    bind group also cannot be built until a viewport is assigned, which is
    why it retries rather than throwing.

    Subclasses supply `uniform_type` and, if the node's position is not
    already a vec3, override `eye_of`.
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

    def on_transform_changed(self, node: NodeT) -> None:
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
        uniform = CameraUniform()
        uniform.projection.data = cast_matrix4(node.projection_matrix)
        uniform.view.data = cast_matrix4(node.view_matrix)
        uniform.position = cast_vec3(self.eye_of(node))

        self.gfx.device.queue.write_buffer(self.uniform_buffer, 0, uniform)
        return True

    def eye_of(self, node: NodeT) -> glm.vec3:
        return node.global_position

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        self.flush()
        if self.bind_group is None:
            raise RuntimeError(
                f"{self!r} has no bind group: "
                f"viewport={self._node.viewport if self._node else None} "
                f"buffer={self.uniform_buffer is not None}"
            )
        self.bind_group.bind(pass_enc)