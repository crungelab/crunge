from ctypes import sizeof
import random

from loguru import logger
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from ... import Renderer
from ...uniforms import cast_matrix4, cast_tuple4f
from ..vu_2d import Vu2D

from ..uniforms_2d import Vec2, ModelUniform, ParticleUniform
from ..binding_2d import EmitterBindGroup
#from ..binding_2d import ModelBindGroup

from ..program_2d import Program2D

from .spawner import Spawner, RadialBurstSpawner

class ParticleSystem2D(Vu2D):
    def __init__(self, program: Program2D, color=(0.0, 0.0, 1.0, 1.0)):
        super().__init__()
        self.color = color
        self.program = program
        self.num_particles = 32
        self.spawner: Spawner = None

        self.model_uniform_buffer: wgpu.Buffer = None
        self.model_uniform_buffer_size: int = 0

        self.particles_buffer: wgpu.Buffer = None

        self.create_spawner()
        self.create_particles()
        self.create_buffers()
        self.create_bind_groups()

    @property
    def size(self):
        return glm.vec2(10, 10)

    def create_spawner(self):
        self.spawner = RadialBurstSpawner(self.color)

    def create_particles(self):
        self.particles = (ParticleUniform * self.num_particles)()
        for i in range(self.num_particles):
            self.spawner(self.particles[i])
    '''
    def create_particles(self):
        self.particles = (ParticleUniform * self.num_particles)()
        for i in range(0, self.num_particles):
            self.particles[i].position = Vec2(0.0, 0.0)
            self.particles[i].velocity = Vec2(
                random.uniform(-1, 1), random.uniform(-1, 1)
            )
            self.particles[i].color = cast_tuple4f(self.color)
            self.particles[i].age = 0.0
            self.particles[i].lifespan = 100.0
    '''

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
        #logger.debug(self.compute_bind_group)

        self.model_bind_group = EmitterBindGroup(
            self.model_uniform_buffer,
            self.model_uniform_buffer_size,
            storage_buffer=self.particles_buffer,
            storage_buffer_size=self.particles_buffer_size,
        )

    '''
    def on_transform(self):
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.gfx.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)
    '''

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        super().bind(pass_enc)
        self.model_bind_group.bind(pass_enc)

    '''
    def _draw(self):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.model_bind_group.bind(pass_enc)
        pass_enc.draw(4, self.num_particles)
    '''

    def _draw(self):
        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4, self.num_particles)

    def update(self, delta_time: float):
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
