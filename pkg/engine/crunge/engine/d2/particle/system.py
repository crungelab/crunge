from ctypes import sizeof
import random

from loguru import logger
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from ... import Renderer
from ...uniforms import cast_tuple4f
from ..vu_2d import Vu2D

from ..uniforms_2d import Vec2, ModelUniform, ParticleUniform
from ..binding_2d import EmitterBindGroup

from ..program_2d import Program2D

from .spawner import Spawner, RadialBurstSpawner


class ParticleSystem2D(Vu2D):
    """Emitter drawn as instanced quads, stepped by a compute pass.

    The transform is not this class's business: it goes into NodeUniform,
    which Vu2D writes to the node buffer. ModelUniform has no transform
    field — only colour and texture description — which is why the old
    `on_transform` override that wrote `model_uniform.transform` was
    commented out rather than fixed.
    """

    def __init__(
        self,
        program: Program2D,
        color=(0.0, 0.0, 1.0, 1.0),
        num_particles: int = 32,
    ):
        super().__init__()
        self.program = program
        self.num_particles = num_particles
        self.spawner: Spawner = None
        self.particles = None

        self.model_uniform_buffer: wgpu.Buffer = None
        self.model_uniform_buffer_size: int = 0

        self.particles_buffer: wgpu.Buffer = None
        self.particles_buffer_size: int = 0

        self.compute_bind_group: wgpu.BindGroup = None
        self.model_bind_group: EmitterBindGroup = None

        # Setter marks GPU dirt, so it comes after the buffer fields exist.
        self.color = color

        # create_spawner/create_particles/create_buffers/create_bind_groups
        # were all called here. The last two acquire GPU resources before
        # the lifecycle has started, and Vu2D._enable calls them again —
        # so every system built two sets of buffers, the second of which
        # the bind groups pointed at while the first leaked.

    @property
    def size(self):
        return glm.vec2(10, 10)

    # -- lifetime ----------------------------------------------------------

    def _create(self):
        super()._create()
        # CPU-side only; the buffers built from this come later, in _enable.
        self.create_spawner()
        self.create_particles()

    def create_spawner(self):
        self.spawner = RadialBurstSpawner(self.color)

    def create_particles(self):
        self.particles = (ParticleUniform * self.num_particles)()
        for i in range(self.num_particles):
            self.spawner(self.particles[i])

    def create_buffers(self):
        super().create_buffers()
        self.particles_buffer = utils.create_buffer_from_ctypes_array(
            self.device, "PARTICLES", self.particles, wgpu.BufferUsage.STORAGE
        )
        self.particles_buffer_size = sizeof(self.particles)
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        super().create_bind_groups()

        compute_bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, buffer=self.particles_buffer),
        ]

        compute_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Compute bind group",
            layout=self.program.compute_pipeline.get_bind_group_layout(0),
            entries=compute_bindgroup_entries,
        )

        self.compute_bind_group = self.device.create_bind_group(compute_bind_group_desc)

        self.model_bind_group = EmitterBindGroup(
            self.model_uniform_buffer,
            self.model_uniform_buffer_size,
            storage_buffer=self.particles_buffer,
            storage_buffer_size=self.particles_buffer_size,
        )

    # -- deferred rebuild --------------------------------------------------

    def _flush_gpu(self) -> bool:
        if self.model_uniform_buffer is None:
            return False
        if not super()._flush_gpu():
            return False

        # Colour only. Each particle already carries its own colour from
        # the spawner, so this is the emitter-wide tint; rect, texture_size
        # and the flags stay at their defaults for an untextured system.
        model_uniform = ModelUniform()
        model_uniform.color = cast_tuple4f(self.color)
        self.gfx.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)
        return True

    # -- frame -------------------------------------------------------------

    def update(self, delta_time: float):
        # Head-call: Vu2D.update flushes pending uploads, and buffer writes
        # have to land before any pass is opened. Without this the node and
        # model uniforms were never written at all.
        super().update(delta_time)

        if self.compute_bind_group is None:
            return

        compute_pass = wgpu.ComputePassDescriptor(
            label="Main Compute Pass",
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()

        compute_pass = encoder.begin_compute_pass(compute_pass)
        compute_pass.set_pipeline(self.program.compute_pipeline)
        compute_pass.set_bind_group(0, self.compute_bind_group)
        compute_pass.dispatch_workgroups(1)
        compute_pass.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self.model_bind_group.bind(pass_enc)

    def _draw(self):
        if self.model_bind_group is None:
            return

        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4, self.num_particles)