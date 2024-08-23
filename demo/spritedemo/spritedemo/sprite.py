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

from .scene_renderer import SceneRenderer
from .vu_2d import Vu2D
from .uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    MeshUniform,
)
from .program import Program
from .texture import Texture

shader_code = """
struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;

@group(1) @binding(0) var mySampler: sampler;
@group(1) @binding(1) var myTexture : texture_2d<f32>;

@group(2) @binding(0) var<uniform> model : mat4x4<f32>;

struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = camera.projection * camera.view * model * in.pos;
  return VertexOutput(vert_pos, in.uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
  return textureSample(myTexture, mySampler, uv);
}
"""

INDICES = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint16)

POINTS = [
    (-0.5, 0.5),  # top-left
    (-0.5, -0.5),  # bottom-left
    (0.5, -0.5),  # bottom-right
    (0.5, 0.5),  # top-right
]

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
        ("texcoord", np.float32, (2,)),  # Texture coordinates (u, v)
    ]
)


@klass.singleton
class SpriteProgram(Program):
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
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
        ]

        material_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(material_bgl_entries), entries=material_bgl_entries
        )
        material_bgl = self.device.create_bind_group_layout(material_bgl_desc)
        logger.debug(f"material_bgl: {material_bgl}")

        mesh_bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        mesh_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(mesh_bgl_entries), entries=mesh_bgl_entries
        )
        mesh_bgl = self.device.create_bind_group_layout(mesh_bgl_desc)
        logger.debug(f"mesh_bgl: {mesh_bgl}")

        self.bind_group_layouts = wgpu.BindGroupLayouts(
            [camera_bgl, material_bgl, mesh_bgl]
        )

    def create_render_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

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

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
            depth_stencil=depth_stencil_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)


class Sprite(Vu2D):
    material_bind_group: wgpu.BindGroup = None
    mesh_bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    indices: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = wgpu.IndexFormat.UINT16

    mesh_uniform_buffer: wgpu.Buffer = None
    mesh_uniform_buffer_size: int = 0

    def __init__(self, texture: Texture) -> None:
        super().__init__()
        self.program = SpriteProgram()
        self._texture = texture
        self.indices = INDICES
        self.points = POINTS
        self.create_vertices()
        self.create_buffers()
        self.create_bind_groups()

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: Texture):
        self._texture = value
        logger.debug(f"Setting texture: {value}")
        self.update_vertices()

    @property
    def size(self):
        return self.texture.size

    @property
    def width(self):
        return self.texture.width

    @property
    def height(self):
        return self.texture.height

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points), dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"] = self.points
        self.vertices["texcoord"] = self.texture.coords

    def update_vertices(self):
        self.create_vertices()
        utils.write_buffer(
            self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes
        )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "INDEX", self.indices, wgpu.BufferUsage.INDEX
        )
        # Uniform Buffers
        self.mesh_uniform_buffer_size = sizeof(MeshUniform)
        self.mesh_uniform_buffer = self.gfx.create_buffer(
            "Mesh Buffer",
            self.mesh_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        view: wgpu.TextureView = self.texture.texture.create_view()
        sampler = self.device.create_sampler()

        material_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=view),
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

        mesh_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.mesh_uniform_buffer,
                    size=self.mesh_uniform_buffer_size,
                ),
            ]
        )

        mesh_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Mesh bind group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(mesh_bindgroup_entries),
            entries=mesh_bindgroup_entries,
        )

        self.mesh_bind_group = self.device.create_bind_group(mesh_bind_group_desc)

    def draw(self, renderer: SceneRenderer):
        # logger.debug("Drawing sprite")
        mesh_uniform = MeshUniform()
        mesh_uniform.model.data = cast_matrix4(self.transform)
        renderer.device.queue.write_buffer(
            self.mesh_uniform_buffer,
            0,
            as_capsule(mesh_uniform),
            self.mesh_uniform_buffer_size,
        )

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.mesh_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.indices))
