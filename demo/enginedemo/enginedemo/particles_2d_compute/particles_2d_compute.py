import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
import random

from loguru import logger
import numpy as np
import glm

from crunge import wgpu
from crunge import imgui

import crunge.wgpu.utils as utils

from crunge.engine import Renderer

from ..demo import Demo

from .data import vertex_data
from .uniforms import Particle, Vec2, Vec4

cs_code = """
struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group(0) @binding(1) var<storage, read_write> particles: array<Particle>;

@compute @workgroup_size(64) // Adjust workgroup size based on your needs
fn cs_main(@builtin(global_invocation_id) global_id : vec3<u32>) {
    let id = global_id.x;
    if (particles[id].age < particles[id].lifespan) {
        particles[id].position += particles[id].velocity;
        particles[id].age += 1.0;
        // Update other properties as needed
    } else {
        // Reset or hide the particle
    }
}
"""

vs_code = """
struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@group(0) @binding(0) var<uniform> uniforms : Uniforms;

struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group(0) @binding(1)  var<storage, read> particles: array<Particle>;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) age: f32,
    @location(2) lifespan: f32,
}

@vertex
fn vs_main(@location(0) pos: vec2f, @builtin(instance_index) index: u32) -> VertexOutput {
    var output: VertexOutput;
    let vert_pos = pos + particles[index].position;
    output.position = uniforms.modelViewProjectionMatrix * vec4<f32>(vert_pos.x, vert_pos.y, 0.0, 1.0);
    output.color = particles[index].color;
    output.age = particles[index].age;
    output.lifespan = particles[index].lifespan;
    return output;
}
"""

fs_code = """
struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) age: f32,
    @location(2) lifespan: f32,
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    //return inColor;
    let fadeFactor: f32 = 1.0 - (in.age / in.lifespan);
    let outColor = vec4<f32>(in.color.rgb, in.color.a * fadeFactor);
    // Optionally clamp fadeFactor to avoid negative values
    // fadeFactor = max(fadeFactor, 0.0);
    return outColor;
}
"""

# TODO: hanging on resize


class ParticlesDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    particles_buffer: wgpu.Buffer = None

    kWidth = 800
    kHeight = 600

    def __init__(self):
        super().__init__()

        self.cs_module = self.gfx.create_shader_module(cs_code)
        self.vs_module = self.gfx.create_shader_module(vs_code)
        self.fs_module = self.gfx.create_shader_module(fs_code)

        self.num_particles = 32

    def create_device_objects(self):
        self.create_particles()
        self.create_buffers()
        self.create_pipeline()

    def reset(self):
        self.create_particles()
        self.create_buffers()
        self.create_pipeline()

    def create_buffers(self):
        logger.debug("create_buffers")
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.particles_buffer = utils.create_buffer_from_ctypes_array(
            self.device, "PARTICLES", self.particles, wgpu.BufferUsage.STORAGE
        )

    def create_particles(self):
        logger.debug("create_particles")
        self.particles = (Particle * self.num_particles)()
        for i in range(0, self.num_particles):
            self.particles[i].position = Vec2(0.0, 0.0)
            self.particles[i].velocity = Vec2(
                random.uniform(-1, 1), random.uniform(-1, 1)
            )
            self.particles[i].color = Vec4(0.0, 0.0, 1.0, 1.0)
            self.particles[i].age = 0.0
            self.particles[i].lifespan = 100.0

    def create_pipeline(self):
        logger.debug("create_pipeline")

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
        ]

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=2 * sizeof(c_float),
                attribute_count=1,
                attributes=vertAttributes,
            )
        ]

        # Compute Bind Group Layout Entries
        compute_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.COMPUTE,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.UNIFORM,
                    min_binding_size=0,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.COMPUTE,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.STORAGE,
                    min_binding_size=0,
                ),
            ),
        ]

        # Render Bind Group Layout
        compute_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(compute_bgl_entries), entries=compute_bgl_entries
        )
        compute_bgl = self.device.create_bind_group_layout(compute_bgl_desc)

        # Render Pipeline Layout
        compute_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=[compute_bgl]
        )

        compute_pl_desc = wgpu.ComputePipelineDescriptor(
            label="Main Compute Pipeline",
            layout=self.device.create_pipeline_layout(compute_pll_desc),
            # compute=wgpu.ProgrammableStageDescriptor(
            compute=wgpu.ComputeState(
                module=self.cs_module,
                entry_point="cs_main",
            ),
        )
        self.compute_pipeline = self.device.create_compute_pipeline(compute_pl_desc)

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

        fragmentState = wgpu.FragmentState(
            module=self.fs_module,
            entry_point="fs_main",
            target_count=1,
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=self.vs_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vb_layouts,
        )

        # Render Bind Group Layout Entries
        render_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.UNIFORM,
                    min_binding_size=0,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.COMPUTE | wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE,
                    min_binding_size=0,
                ),
            ),
        ]

        # Render Bind Group Layout
        render_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(render_bgl_entries), entries=render_bgl_entries
        )
        render_bgl = self.device.create_bind_group_layout(render_bgl_desc)

        # Render Pipeline Layout
        render_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=[render_bgl]
        )

        render_pl_desc = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(render_pll_desc),
            vertex=vertex_state,
            fragment=fragmentState,
        )

        logger.debug(render_pl_desc)
        self.render_pipeline = self.device.create_render_pipeline(render_pl_desc)
        logger.debug(self.render_pipeline)

        bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0, buffer=self.uniformBuffer, size=self.uniformBufferSize
            ),
            wgpu.BindGroupEntry(binding=1, buffer=self.particles_buffer),
        ]

        compute_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Compute bind group",
            layout=self.compute_pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.compute_bind_group = self.device.create_bind_group(compute_bind_group_desc)
        logger.debug(self.compute_bind_group)

        render_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Render bind group",
            layout=self.render_pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.render_bind_group = self.device.create_bind_group(render_bind_group_desc)
        logger.debug(self.render_bind_group)

        # exit()

    def draw(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                # view=renderer.texture_view,
                view=renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()

        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.render_pipeline)
        pass_enc.set_bind_group(0, self.render_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(6, self.num_particles)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        self.draw_gui()
        super().draw(renderer)

    def draw_gui(self):
        imgui.begin("Sparks")
        if imgui.button("Run"):
            self.reset()
        imgui.end()

    def frame(self):
        model = glm.mat4(1.0)  # Identity matrix
        x = self.width / 2
        y = self.height / 2
        model = glm.translate(model, glm.vec3(x, y, 0))
        # model = glm.rotate(model, glm.radians(45.0), glm.vec3(0, 0, 1))
        model = glm.scale(model, glm.vec3(2, 2, 1))
        view = glm.mat4(1.0)  # Identity matrix

        viewport_width = self.width
        viewport_height = self.height

        ortho_left = 0
        ortho_right = viewport_width
        ortho_bottom = 0
        ortho_top = viewport_height
        ortho_near = -1  # Near clipping plane
        ortho_far = 1  # Far clipping plane

        projection = glm.ortho(
            ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far
        )

        transform = projection * view * model

        self.device.queue.write_buffer(self.uniformBuffer, 0, transform)

        super().frame()

    def update(self, delta_time: float):
        compute_pass = wgpu.ComputePassDescriptor(
            label="Main Compute Pass",
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()

        compute_pass = encoder.begin_compute_pass(compute_pass)
        compute_pass.set_pipeline(self.compute_pipeline)
        compute_pass.set_bind_group(0, self.compute_bind_group)
        # compute_pass.dispatch(workgroupCountX, workgroupCountY, workgroupCountZ);
        # compute_pass.dispatch_workgroups(4, 4, 1)
        compute_pass.dispatch_workgroups(1)
        compute_pass.end()
        commands = encoder.finish()
        self.queue.submit(1, commands)


def main():
    ParticlesDemo().create().run()


if __name__ == "__main__":
    main()
