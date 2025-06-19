from ctypes import sizeof
import random

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine import Renderer

from crunge.engine.d2.vu_2d import Vu2D
from crunge.engine.uniforms import cast_matrix4, cast_vec4
from crunge.engine.d2.uniforms_2d import (
    ModelUniform,
)
from crunge.engine.d2.bindings import EmitterBindGroup, EmitterBindGroupLayout
from crunge.engine.loader.shader_loader import ShaderLoader

from .uniforms import Particle, Vec2
from ...demo_program import DemoProgram


@klass.singleton
class ExplosionProgram(DemoProgram):
    def __init__(self):
        super().__init__()
        logger.debug("ExplosionProgram.__init__")
        self.cs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "explosion.comp.wgsl"
        )
        self.vs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "explosion.vert.wgsl"
        )
        self.fs_module = ShaderLoader(self.template_env, self.template_dict).load(
            "explosion.frag.wgsl"
        )

        self.create_render_pipeline()
        self.create_compute_bind_group_layouts()
        self.create_compute_pipeline()

    @property
    def model_bind_group_layout(self):
        return EmitterBindGroupLayout()

    def create_render_pipeline(self):
        blend_state = wgpu.BlendState(
            alpha=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.ONE,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
            color=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.SRC_ALPHA,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
        )

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
                write_mask=wgpu.ColorWriteMask.ALL,
            )
        ]

        fragment_state = wgpu.FragmentState(
            module=self.fs_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=self.vs_module,
            entry_point="vs_main",
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=True,
            depth_compare=wgpu.CompareFunction.LESS,
        )

        # Render Pipeline Layout
        render_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.bind_group_layouts
        )

        render_pl_desc = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(render_pll_desc),
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragment_state,
            depth_stencil=depth_stencil_state,
        )

        logger.debug(render_pl_desc)
        self.render_pipeline = self.device.create_render_pipeline(render_pl_desc)
        logger.debug(self.render_pipeline)

    def create_compute_bind_group_layouts(self):
        # Compute Bind Group Layout Entries
        compute_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.COMPUTE,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.STORAGE,
                    min_binding_size=0,
                ),
            ),
        ]

        # Compute Bind Group Layout
        compute_bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=compute_bgl_entries)
        compute_bgl = self.device.create_bind_group_layout(compute_bgl_desc)

        self.compute_bind_group_layouts = [compute_bgl]

    def create_compute_pipeline(self):

        # Compute Pipeline Layout
        compute_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=self.compute_bind_group_layouts
        )

        compute_pl_desc = wgpu.ComputePipelineDescriptor(
            label="Main Compute Pipeline",
            layout=self.device.create_pipeline_layout(compute_pll_desc),
            compute=wgpu.ComputeState(
                module=self.cs_module,
                entry_point="cs_main",
            ),
        )
        self.compute_pipeline = self.device.create_compute_pipeline(compute_pl_desc)
        logger.debug(self.compute_pipeline)


class ExplosionVu(Vu2D):
    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    particles_buffer: wgpu.Buffer = None

    def __init__(self, color: glm.vec4 = glm.vec4(0.0, 0.0, 1.0, 1.0)):
        super().__init__()
        self.color = color
        self.program = ExplosionProgram()

        self.num_particles = 32
        self.create_particles()
        self.create_buffers()
        self.create_bindgroups()

    @property
    def size(self):
        return glm.vec2(10, 10)

    def create_particles(self):
        logger.debug("create_particles")
        self.particles = (Particle * self.num_particles)()
        for i in range(0, self.num_particles):
            self.particles[i].position = Vec2(0.0, 0.0)
            self.particles[i].velocity = Vec2(
                random.uniform(-1, 1), random.uniform(-1, 1)
            )
            self.particles[i].color = cast_vec4(self.color)
            self.particles[i].age = 0.0
            self.particles[i].lifespan = 100.0

    def create_buffers(self):
        logger.debug("create_buffers")
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

    def create_bindgroups(self):
        compute_bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, buffer=self.particles_buffer),
        ]

        compute_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Compute bind group",
            layout=self.program.compute_pipeline.get_bind_group_layout(0),
            entries=compute_bindgroup_entries,
        )

        self.compute_bind_group = self.device.create_bind_group(compute_bind_group_desc)
        logger.debug(self.compute_bind_group)

        self.model_bind_group = EmitterBindGroup(
            self.model_uniform_buffer,
            self.model_uniform_buffer_size,
            storage_buffer=self.particles_buffer,
            storage_buffer_size=self.particles_buffer_size,
        )

    def on_transform(self):
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.gfx.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)

    def draw(self, renderer: Renderer):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline)
        self.model_bind_group.bind(pass_enc)
        pass_enc.draw(4, self.num_particles)

    def update(self, delta_time: float):
        # logger.debug("explosion update")
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
