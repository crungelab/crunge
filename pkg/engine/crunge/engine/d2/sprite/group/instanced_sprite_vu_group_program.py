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

from ...program_2d import Program2D
from ....resource.bind_group.bind_group_layout import BindGroupLayout

shader_code = """
struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    viewport : vec2<f32>,
    position: vec3<f32>,
}

struct Model {
    transform : mat4x4<f32>,
}

struct Material {
    color : vec4<f32>,
    spriteRect : vec4<f32>, // x, y, width, height
    textureSize : vec2<f32>,
    flipH : u32, // 1 = true, 0 = false
    flipV : u32, // 1 = true, 0 = false
}

@group(0) @binding(0) var<uniform> camera : Camera;

@group(1) @binding(0) var mySampler: sampler;
@group(1) @binding(1) var myTexture : texture_2d<f32>;
@group(1) @binding(2) var<uniform> material : Material;

@group(2) @binding(0) var<storage, read> models: array<Model>;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

// Function to compute UV coordinates with optional flipping
fn compute_uv(idx: u32, rect: vec4<f32>, tex_size: vec2<f32>, flip_h: bool, flip_v: bool) -> vec2<f32> {
    // Normalized texture coordinates with half-pixel offsets
    let u0 = (rect.x + 0.5) / tex_size.x;
    let u1 = (rect.x + rect.z - 0.5) / tex_size.x;
    let v0 = (rect.y + 0.5) / tex_size.y;
    let v1 = (rect.y + rect.w - 0.5) / tex_size.y;

    // Flip the V coordinates
    let v0_flipped = v1;
    let v1_flipped = v0;

    // Reorder UVs for triangle strip
    var uvs = array<vec2<f32>, 4>(
        vec2<f32>(u0, v0_flipped), // Bottom-left
        vec2<f32>(u1, v0_flipped), // Bottom-right
        vec2<f32>(u0, v1_flipped), // Top-left
        vec2<f32>(u1, v1_flipped)  // Top-right
    );

    // Flip horizontally
    if (flip_v) {
        uvs = array<vec2<f32>, 4>(
            uvs[3], // Top-left -> Top-right
            uvs[2], // Bottom-left -> Bottom-right
            uvs[1], // Bottom-right -> Bottom-left
            uvs[0]  // Top-right -> Top-left
        );
    }

    // Flip vertically
    if (flip_h) {
        uvs = array<vec2<f32>, 4>(
            uvs[1], // Top-left -> Bottom-left
            uvs[0], // Bottom-left -> Top-left
            uvs[3], // Bottom-right -> Top-right
            uvs[2]  // Top-right -> Bottom-right
        );
    }

    return uvs[idx];
}

@vertex
fn vs_main(@builtin(vertex_index) vertexIndex: u32, @builtin(instance_index) instanceIndex: u32) -> VertexOutput {
    let x = f32((vertexIndex & 1u) << 1) - 1.0; // Generates -1.0 or 1.0
    let y = f32((vertexIndex & 2u) >> 1) * 2.0 - 1.0; // Generates -1.0 or 1.0

    let quad_pos = vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0); // Scale quad by 0.5
    let vert_pos = camera.projection * camera.view * models[instanceIndex].transform * quad_pos;

    // Extract UV coordinates from the vec4 (only use x and y)
    // Compute UV for the current vertex with flipping
    let uv = compute_uv(
        vertexIndex,
        material.spriteRect,
        material.textureSize,
        material.flipH != 0u,
        material.flipV != 0u
    );

    return VertexOutput(vert_pos, uv);
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let color = textureSample(myTexture, mySampler, in.uv);
    return color * material.color;
}
"""

@klass.singleton
class ModelBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        model_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                #buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.READ_ONLY_STORAGE),
            ),
        ]

        model_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(model_bgl_entries), entries=model_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(model_bgl_desc)
        logger.debug(f"model_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)

@klass.singleton
class InstancedSpriteVuGroupProgram(Program2D):
    pipeline: wgpu.RenderPipeline = None

    def __init__(self):
        super().__init__()
        self.create_render_pipeline()

    @property
    def model_bind_group_layout(self):
        return ModelBindGroupLayout().get()

    def create_render_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

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
