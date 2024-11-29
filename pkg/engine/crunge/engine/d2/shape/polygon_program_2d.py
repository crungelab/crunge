from ctypes import sizeof, c_float

from loguru import logger

from crunge.core import klass
from crunge import wgpu

from crunge.engine.d2.program_2d import Program2D

from ...resource.bind_group.bind_group_layout import BindGroupLayout


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

@group(1) @binding(0) var<uniform> material : Material;

@group(2) @binding(0) var<uniform> model : Model;

struct VertexInput {
  @location(0) pos: vec4<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = camera.projection * camera.view * model.transform * in.pos;
  return VertexOutput(vert_pos);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    return material.color;
}
"""

@klass.singleton
class MaterialBindGroupLayout(BindGroupLayout):
    def __init__(self) -> None:
        material_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        material_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(material_bgl_entries), entries=material_bgl_entries
        )
        bind_group_layout = self.device.create_bind_group_layout(material_bgl_desc)
        logger.debug(f"material_bgl: {bind_group_layout}")
        super().__init__(bind_group_layout)


@klass.singleton
class PolygonProgram2D(Program2D):
    pipeline: wgpu.RenderPipeline = None

    def __init__(self):
        super().__init__()
        self.create_render_pipeline()

    @property
    def material_bind_group_layout(self):
        return MaterialBindGroupLayout().get()

    def create_render_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
        ]

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=2 * sizeof(c_float),
                attribute_count=len(vertAttributes),
                attributes=vertAttributes,
            )
        ]

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
            buffer_count=1,
            buffers=vertBufferLayouts,
        )

        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
        )

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=len(self.bind_group_layouts),
            bind_group_layouts=self.bind_group_layouts,
        )

        #primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.LINE_LIST)
        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.LINE_STRIP)

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            primitive=primitive,
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)
