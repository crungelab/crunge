from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

from loguru import logger

from crunge.core import klass
from crunge import wgpu

from ..program_2d import Program2D

shader_code = """
struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    position: vec3<f32>,
}

struct Model {
    transform : mat4x4<f32>,
}

struct Material {
    color : vec4<f32>,
    uvs : array<vec4<f32>, 4>, // Use vec4<f32> for proper alignment
}

@group(0) @binding(0) var<uniform> camera : Camera;

@group(1) @binding(0) var mySampler: sampler;
@group(1) @binding(1) var myTexture : texture_2d<f32>;
@group(1) @binding(2) var<uniform> material : Material;

@group(2) @binding(0) var<uniform> model : Model;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> VertexOutput {
    let x = f32((idx & 1u) << 1) - 1.0; // Generates -1.0 or 1.0
    let y = f32((idx & 2u) >> 1) * 2.0 - 1.0; // Generates -1.0 or 1.0

    let quad_pos = vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0); // Scale quad by 0.5
    let vert_pos = camera.projection * camera.view * model.transform * quad_pos;

    // Extract UV coordinates from the vec4 (only use x and y)
    let uv = material.uvs[idx].xy;

    return VertexOutput(vert_pos, uv);
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y); // Flip Y-axis for correct texture orientation
    let color = textureSample(myTexture, mySampler, uv);
    return color * material.color;
}
"""

'''
shader_code = """
struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    position: vec3<f32>,
}

struct Model {
    transform : mat4x4<f32>,
}

struct Material {
    color : vec4<f32>,
}

@group(0) @binding(0) var<uniform> camera : Camera;

@group(1) @binding(0) var mySampler: sampler;
@group(1) @binding(1) var myTexture : texture_2d<f32>;
@group(1) @binding(2) var<uniform> material : Material;

@group(2) @binding(0) var<uniform> model : Model;

struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    let x = f32((idx & 1u) << 1) - 1.0; // Generates 0 or 1, then maps to -1 or 1
    let y = f32((idx & 2u) >> 1) * 2.0 - 1.0; // Generates 0 or 1, then maps to -1 or 1
    //return vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0); //Scale by 0.5 to make the quad half the size
    let quad_pos = vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0);
    let vert_pos = camera.projection * camera.view * model.transform * quad_pos;
    return vert_pos;
}

/*
@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = camera.projection * camera.view * model.transform * in.pos;
  return VertexOutput(vert_pos, in.uv);
}
*/

@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}

/*
@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
    let color = textureSample(myTexture, mySampler, uv);
    return color * material.color;
}
*/
"""
'''


@klass.singleton
class SpriteProgram(Program2D):
    pipeline: wgpu.RenderPipeline = None

    def __init__(self):
        super().__init__()
        self.create_render_pipeline()

    def create_render_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        '''
        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2,
                offset=2 * sizeof(c_float),
                shader_location=1,
            ),
        ]

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=4 * sizeof(c_float),
                attribute_count=len(vertAttributes),
                attributes=vertAttributes,
            )
        ]
        '''

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
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

        '''
        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayouts,
        )
        '''

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
        )

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=len(self.bind_group_layouts),
            bind_group_layouts=self.bind_group_layouts,
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragmentState,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)
