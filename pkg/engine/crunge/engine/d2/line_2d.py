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
import numpy as np
import glm

from crunge.core import klass
from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..math import Point2, Size2
from ..program import Program
from ..resource.texture import Texture

from .renderer_2d import Renderer2D
from .vu_2d import Vu2D
from .uniforms_2d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    cast_vec4,
    ModelUniform,
    MaterialUniform,
)

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

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
    ]
)


@klass.singleton
class Line2DProgram(Program):
    pipeline: wgpu.RenderPipeline = None

    def __init__(self):
        super().__init__()
        self.create_render_bind_group_layouts()
        self.create_render_pipeline()

    def create_render_bind_group_layouts(self):
        camera_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        camera_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(camera_bgl_entries), entries=camera_bgl_entries
        )
        camera_bgl = self.device.create_bind_group_layout(camera_bgl_desc)
        logger.debug(f"camera_bgl: {camera_bgl}")

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
        material_bgl = self.device.create_bind_group_layout(material_bgl_desc)
        logger.debug(f"material_bgl: {material_bgl}")

        model_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        model_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(model_bgl_entries), entries=model_bgl_entries
        )
        model_bgl = self.device.create_bind_group_layout(model_bgl_desc)
        logger.debug(f"model_bgl: {model_bgl}")

        self.bind_group_layouts = wgpu.BindGroupLayouts(
            [camera_bgl, material_bgl, model_bgl]
        )

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

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.LINE_LIST)

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            primitive=primitive,
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)


class Line2D(Vu2D):
    material_bind_group: wgpu.BindGroup = None
    model_bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    material_uniform_buffer: wgpu.Buffer = None
    material_uniform_buffer_size: int = 0

    def __init__(
        self, begin: glm.vec2, end: glm.vec2, color=glm.vec4(1.0, 1.0, 1.0, 1.0)
    ) -> None:
        super().__init__()
        self.begin = begin
        self.end = end
        self.points = [begin, end]
        self.color = color
        self.program = Line2DProgram()
        self.create_vertices()
        self.create_buffers()
        self.create_bind_groups()

    @property
    def size(self) -> Size2:
        return Size2(1.0, 1.0)

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points), dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"] = self.points

    def update_vertices(self):
        self.create_vertices()
        utils.write_buffer(
            self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes
        )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

        self.material_uniform_buffer_size = sizeof(MaterialUniform)
        self.material_uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.material_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        material_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.material_uniform_buffer,
                    size=self.material_uniform_buffer_size,
                ),
            ]
        )

        material_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material bind group",
            layout=self.program.pipeline.get_bind_group_layout(1),
            entry_count=len(material_bindgroup_entries),
            entries=material_bindgroup_entries,
        )

        self.material_bind_group = self.device.create_bind_group(
            material_bind_group_desc
        )

        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.model_uniform_buffer,
                    size=self.model_uniform_buffer_size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Mesh bind group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bind_group_desc)

    def draw(self, renderer: Renderer2D):
        # logger.debug("Drawing sprite")
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        renderer.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )

        material_uniform = MaterialUniform()
        material_uniform.color = cast_vec4(self.color)

        renderer.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            as_capsule(material_uniform),
            self.material_uniform_buffer_size,
        )

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.model_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(2, 1, 0, 0)  # Drawing 2 vertices (a single line)
