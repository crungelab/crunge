from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu

from ..renderer import Renderer
from ..uniforms import cast_matrix4

from .renderer.task.transmissive_phase_3d import TransmissivePhase3D, Transmissive3D

from .program_3d import Program3D
from .vu_3d import Vu3D
from .uniforms_3d import (
    ModelUniform,
)
from .mesh_3d import Mesh3D


@klass.singleton
class MeshInstance3DProgram(Program3D):
    pass


class MeshVu3D(Vu3D):
    def __init__(self, mesh: Mesh3D = None) -> None:
        super().__init__()
        self.model_bind_group: wgpu.BindGroup = None
        self.model_uniform_buffer: wgpu.Buffer = None
        self.model_uniform_buffer_size: int = 0
        self._mesh: Mesh3D = mesh
        self.deferred = False

        # The program, the uniform buffer and the bind group were all built
        # here — GPU resources acquired before the lifetime has started.

    @property
    def mesh(self) -> Mesh3D:
        return self._mesh

    @mesh.setter
    def mesh(self, mesh: Mesh3D):
        self._mesh = mesh
        if mesh is not None:
            # NOTE: mesh.bounds is local. The commented-out update_bounds
            # mapped it through the transform; if bounds are used for
            # culling, this wants to_global(self.transform).
            self.bounds = mesh.bounds
        self.mark_gpu()

    # -- lifetime ----------------------------------------------------------
    #
    # If Vu3D._enable already calls create_program/create_buffers/
    # create_bind_groups the way Vu2D does, drop this override and let the
    # base drive them — otherwise they run twice.

    def _create(self):
        super()._create()
        self.create_program()
        self.create_buffers()
        self.create_bind_groups()

    def create_program(self):
        self.program = MeshInstance3DProgram()

    def create_buffers(self):
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Uniform Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        logger.debug("Creating bind group")

        model_bg_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.model_uniform_buffer,
                size=self.model_uniform_buffer_size,
            ),
        ]

        model_bg_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.model_bind_group_layout,
            entries=model_bg_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bg_desc)

    # -- deferred rebuild --------------------------------------------------

    def on_transform(self):
        # Was calling gpu_update_model directly. Record and mark; the write
        # lands in flush, before the render pass opens.
        super().on_transform()
        self.mark_gpu()

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        self.flush()

    def gpu_update_model(self):
        """Deferred alias, kept so older callers keep working. Delete once
        `rg gpu_update_model` comes back clean."""
        self.mark_gpu()

    def _flush_gpu(self) -> bool:
        if self.model_uniform_buffer is None:
            return False

        model_matrix = self.transform
        logger.debug(f"mesh flush: transform[3]={model_matrix[3]}")

        normal_matrix = glm.mat4(glm.transpose(glm.inverse(glm.mat3(model_matrix))))

        model_uniform = ModelUniform()
        model_uniform.model_matrix.data = cast_matrix4(model_matrix)
        model_uniform.normal_matrix.data = cast_matrix4(normal_matrix)

        self.gfx.device.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)
        return True

    # -- frame -------------------------------------------------------------

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(3, self.model_bind_group)

    def _draw(self):
        if self._mesh is None or self.model_bind_group is None:
            return

        renderer = Renderer.get_current()

        pass_enc = renderer.pass_enc
        self.bind(pass_enc)

        for primitive in self._mesh.primitives:
            primitive.draw()

        super()._draw()

    def draw(self):
        if self.deferred:
            phase: TransmissivePhase3D = self.current_renderer.plan.get_phase(
                TransmissivePhase3D
            )
            phase.add(Transmissive3D(self, self._draw))
        else:
            self._draw()