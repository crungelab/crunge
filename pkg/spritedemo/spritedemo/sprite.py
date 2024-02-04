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

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .scene_renderer import SceneRenderer
from .vu_2d import Vu2D
from .camera_2d import Camera2D
from .uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    LightUniform,
)
from .texture import Texture

shader_code = """
struct Camera {
    modelMatrix : mat4x4<f32>,
    transformMatrix : mat4x4<f32>,
    normalMatrix: mat3x3<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;

@group(0) @binding(1) var mySampler: sampler;
@group(0) @binding(2) var myTexture : texture_2d<f32>;

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
  let vert_pos = camera.transformMatrix * in.pos;
  return VertexOutput(vert_pos, in.uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
  return textureSample(myTexture, mySampler, uv);
}
"""

INDICES = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint16)

'''
vertices = np.array(
    [
        -0.5,  0.5,  0.0, 1.0, # top-left
        -0.5, -0.5,  0.0, 0.0, # bottom-left
        0.5, -0.5,  1.0, 0.0, # bottom-right
        0.5,  0.5,  1.0, 1.0, # top-right
    ],
    dtype=np.float32,
)
'''

POINTS = [
    (-0.5, 0.5),  # top-left
    (-0.5, -0.5), # bottom-left
    (0.5, -0.5),  # bottom-right
    (0.5, 0.5)    # top-right
]

# Define the structured dtype for the combined data
vertex_dtype = np.dtype([
    ('position', np.float32, (2,)),  # Points (x, y)
    ('texcoord', np.float32, (2,))   # Texture coordinates (u, v)
])


class Sprite(Vu2D):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    indices: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = wgpu.IndexFormat.UINT16

    camera_uniform_buffer: wgpu.Buffer = None
    camera_uniform_buffer_size: int = 0

    def __init__(self, texture: Texture) -> None:
        super().__init__()
        self._texture = texture
        self.indices = INDICES
        self.points = POINTS
        self.create_vertices()
        self.create_buffers()
        self.create_pipeline()

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
        self.vertices['position'] = self.points
        self.vertices['texcoord'] = self.texture.coords

    def update_vertices(self):
        self.create_vertices()
        utils.write_buffer(self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes)

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "INDEX", self.indices, wgpu.BufferUsage.INDEX
        )
        # Uniform Buffers
        self.camera_uniform_buffer_size = sizeof(CameraUniform)
        self.camera_uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.camera_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)
        sampler = self.device.create_sampler()

        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
                ),
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X2,
                    offset=2 * sizeof(c_float),
                    shader_location=1,
                ),
            ]
        )

        vertBufferLayout = wgpu.VertexBufferLayout(
            array_stride=4 * sizeof(c_float),
            attribute_count=len(vertAttributes),
            attributes=vertAttributes[0],
        )

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

        colorTargetState = wgpu.ColorTargetState(
            format=wgpu.TextureFormat.BGRA8_UNORM,
            blend=blend_state,
            write_mask=wgpu.ColorWriteMask.ALL,
        )

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetState,
        )

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayout,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
        )

        bgl_entries = wgpu.BindGroupLayoutEntries(
            [
                wgpu.BindGroupLayoutEntry(
                    binding=0,
                    visibility=wgpu.ShaderStage.VERTEX,
                    buffer=wgpu.BufferBindingLayout(
                        type=wgpu.BufferBindingType.UNIFORM
                    ),
                ),
                wgpu.BindGroupLayoutEntry(
                    binding=1,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    sampler=wgpu.SamplerBindingLayout(
                        type=wgpu.SamplerBindingType.FILTERING
                    ),
                ),
                wgpu.BindGroupLayoutEntry(
                    binding=2,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    texture=wgpu.TextureBindingLayout(
                        sample_type=wgpu.TextureSampleType.FLOAT,
                        view_dimension=wgpu.TextureViewDimension.E2D,
                    ),
                ),
            ]
        )

        bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(bgl_entries), entries=bgl_entries[0]
        )
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=bgl
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
            depth_stencil=depthStencilState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        view: wgpu.TextureView = self.texture.texture.create_view()

        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0, buffer=self.camera_uniform_buffer, size=self.camera_uniform_buffer_size
                ),
                wgpu.BindGroupEntry(binding=1, sampler=sampler),
                wgpu.BindGroupEntry(binding=2, texture_view=view),
            ]
        )

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries[0],
        )

        self.bind_group = self.device.create_bind_group(bind_group_desc)
        logger.debug(self.bind_group)

        # exit()


    def draw(self, renderer: SceneRenderer):
        #logger.debug("Drawing sprite")
        camera = renderer.camera
        pass_enc = renderer.pass_enc

        model_matrix = self.transform
        transform_matrix = camera.transform_matrix * self.transform
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(model_matrix)))

        camera_uniform = CameraUniform()
        camera_uniform.model_matrix.data = cast_matrix4(model_matrix)
        camera_uniform.transform_matrix.data = cast_matrix4(transform_matrix)
        camera_uniform.normal_matrix.data = cast_matrix3(normal_matrix)

        #camera_uniform.position.x = camera.position.x
        #camera_uniform.position.y = camera.position.y
        #camera_uniform.position.z = camera.position.z
        #camera_uniform.position = cast_vec3(camera.position)
        camera_uniform.position = cast_vec3(glm.vec3(camera.position.x, camera.position.y, 0))

        renderer.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.indices))
