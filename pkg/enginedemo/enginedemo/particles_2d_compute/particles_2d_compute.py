import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys

from loguru import logger
import numpy as np

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine import Renderer

from ..demo import Demo

from .data import vertex_data

cs_code = """
@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;

struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}

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
struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}

@binding(0) @group(0) var<storage, read> particles: array<Particle>;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
}

@vertex
fn vs_main(@location(0) pos: vec2f, @builtin(instance_index) index: u32) -> VertexOutput {
    var output: VertexOutput;
    //let pos = particles[index].position;
    output.position = vec4<f32>(pos.x, pos.y, 0.0, 1.0);
    output.color = particles[index].color;
    return output;
}
"""

fs_code = """
@fragment
fn fs_main(@location(0) inColor: vec4<f32>) -> @location(0) vec4<f32> {
    return inColor;
}
"""

particles_data = np.array(
    [
        # position, velocity, color, age, lifespan
        [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 100.0],
        [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 100.0],
        [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 100.0],
        [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 100.0],
    ],
    dtype=np.float32,
)

class ParticlesDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    #index_buffer: wgpu.Buffer = None
    particles_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    kWidth = 800
    kHeight = 600

    def __init__(self):
        super().__init__()

        #self.num_particles = len(particles_data)
        self.num_particles = 4

        self.create_buffers()
        #self.create_textures()

        cs_module = self.gfx.create_shader_module(cs_code)
        vs_module = self.gfx.create_shader_module(vs_code)
        fs_module = self.gfx.create_shader_module(fs_code)
        
        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
                ),
            ]
        )
        vertBufferLayout = wgpu.VertexBufferLayout(
            array_stride=2 * sizeof(c_float),
            attribute_count=1,
            attributes=vertAttributes[0],
        )

        # Compute Bind Group Layout Entries
        compute_bgl_entries = wgpu.BindGroupLayoutEntries(
            [
                wgpu.BindGroupLayoutEntry(
                    binding=0,
                    visibility=wgpu.ShaderStage.COMPUTE,
                    buffer=wgpu.BufferBindingLayout(
                        type=wgpu.BufferBindingType.STORAGE,
                        min_binding_size=0,
                    ),
                ),
            ]
        )
        # Render Bind Group Layout
        compute_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(compute_bgl_entries), entries=compute_bgl_entries[0]
        )
        compute_bgl = self.device.create_bind_group_layout(compute_bgl_desc)

        # Render Pipeline Layout
        compute_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=compute_bgl
        )

        compute_pl_desc = wgpu.ComputePipelineDescriptor(
            label="Main Compute Pipeline",
            layout=self.device.create_pipeline_layout(compute_pll_desc),
            compute=wgpu.ProgrammableStageDescriptor(
                module=cs_module,
                entry_point="cs_main",
            ),
        )
        self.compute_pipeline = self.device.create_compute_pipeline(compute_pl_desc)

        colorTargetState = wgpu.ColorTargetState(
            format=wgpu.TextureFormat.BGRA8_UNORM,
        )

        fragmentState = wgpu.FragmentState(
            module=fs_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetState,
        )

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayout,
        )

        # Render Bind Group Layout Entries
        render_bgl_entries = wgpu.BindGroupLayoutEntries(
            [
                wgpu.BindGroupLayoutEntry(
                    binding=0,
                    visibility=wgpu.ShaderStage.COMPUTE | wgpu.ShaderStage.VERTEX,
                    buffer=wgpu.BufferBindingLayout(
                        type=wgpu.BufferBindingType.READ_ONLY_STORAGE,
                        min_binding_size=0,
                    ),
                ),
            ]
        )
        # Render Bind Group Layout
        render_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(render_bgl_entries), entries=render_bgl_entries[0]
        )
        render_bgl = self.device.create_bind_group_layout(render_bgl_desc)

        # Render Pipeline Layout
        render_pll_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=render_bgl
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

        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, buffer=self.particles_buffer),
            ]
        )

        compute_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Compute bind group",
            layout=self.compute_pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries[0],
        )

        self.compute_bind_group = self.device.create_bind_group(compute_bind_group_desc)
        logger.debug(self.compute_bind_group)

        render_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Render bind group",
            layout=self.render_pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries[0],
        )

        self.render_bind_group = self.device.create_bind_group(render_bind_group_desc)
        logger.debug(self.render_bind_group)

        # exit()

    def create_buffers(self):
        logger.debug("create_buffers")
        self.particles_buffer = utils.create_buffer_from_ndarray(
            self.device, "PARTICLES", particles_data, wgpu.BufferUsage.STORAGE
        )
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

    def draw(self, renderer: Renderer):
        attachment = wgpu.RenderPassColorAttachment(
            view=renderer.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=attachment,
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

        super().draw(renderer)

    def update(self, delta_time: float):
        compute_pass = wgpu.ComputePassDescriptor(
            label="Main Compute Pass",
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()

        compute_pass = encoder.begin_compute_pass(compute_pass)
        compute_pass.set_pipeline(self.compute_pipeline)
        compute_pass.set_bind_group(0, self.compute_bind_group)
        #compute_pass.dispatch(workgroupCountX, workgroupCountY, workgroupCountZ);
        compute_pass.dispatch_workgroups(4, 4, 1)
        compute_pass.end()
        commands = encoder.finish()
        self.queue.submit(1, commands)


def main():
    ParticlesDemo().create().run()


if __name__ == "__main__":
    main()
