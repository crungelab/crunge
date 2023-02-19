import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .builder import Builder
#from . import utils
from .scene import Scene
from .mesh import Mesh
from .texture_builder import TextureBuilder


shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture : texture_2d<f32>;

struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

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
  let vert_pos = uniforms.modelViewProjectionMatrix * in.pos;
  return VertexOutput(vert_pos, in.uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
  return textureSample(myTexture, mySampler, uv);
}
"""

class Position(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
    ]

class UvCoord(Structure):
    _fields_ = [
        ("u", c_float),
        ("v", c_float),
    ]

class Vertex(Structure):
    _fields_ = [
        ("pos", Position),
        ("uv", UvCoord),
    ]

#kWidth = 1024
#kHeight = 768

kPositionByteOffset = Vertex.pos.offset
kUVByteOffset = Vertex.uv.offset
kVertexDataStride = sizeof(Vertex)

class MeshBuilder(Builder):
    mesh: Mesh

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.mesh = Mesh()
    
    def build(self, tm_mesh: tm.Trimesh):
        mesh: Mesh = self.mesh
        logger.debug(tm_mesh.__dict__)

        #Vertices
        vertices = tm_mesh.vertices.astype(np.float32)
        logger.debug(f'vertices type: {type(vertices)}')
        logger.debug(f'vertices:  {vertices}')
        n_vertices =  len(vertices)
        logger.debug(f'n_vertices:  {n_vertices}')

        # Texture Coordinates
        uv_coords = tm_mesh.visual.uv.astype(np.float32)
        uv_coords = (uv_coords - np.min(uv_coords))/(np.max(uv_coords) - np.min(uv_coords))

        logger.debug(f'uv_coords type: {type(uv_coords)}')
        logger.debug(f'uv_coords:  {uv_coords}')
        n_uv_coords = len(uv_coords)
        logger.debug(f'n_uv_coords:  {n_uv_coords}')

        # Vertex Data
        vertex_data = np.concatenate((vertices, uv_coords), axis=1)
        logger.debug(type(vertex_data))
        logger.debug(f'vertex_data:  {vertex_data}')
        mesh.vertex_data = vertex_data
        mesh.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, vertex_data, wgpu.BufferUsage.VERTEX
        )

        #exit()
        
        # Indices
        indices = tm_mesh.faces.astype(np.uint32)
        logger.debug(f'indices:  {indices}')
        n_indices = self.n_indices = len(indices)
        logger.debug(f'n_indices:  {n_indices}')
        mesh.index_data = indices
        mesh.index_buffer = utils.create_buffer_from_ndarray(
            self.device, indices, wgpu.BufferUsage.INDEX
        )

        # Uniform Buffer

        uniform_buffer_size = 4 * 16
        mesh.uniform_buffer_size = uniform_buffer_size
        
        uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        mesh.uniform_buffer = uniform_buffer

        pipeline = self.create_pipeline()
        mesh.pipeline = pipeline

        visual = tm_mesh.visual
        logger.debug(tm_mesh.visual.__dict__)
        material = visual.material
        logger.debug(material.__dict__)

        texture = TextureBuilder().build(material)

        bg_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=texture.sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=texture.view),
                wgpu.BindGroupEntry(binding=2, buffer=uniform_buffer, size=uniform_buffer_size),
            ]
        )

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture+Uniform bind group",
            layout=pipeline.get_bind_group_layout(0),
            entry_count=len(bg_entries),
            entries=bg_entries[0],
        )

        mesh.bind_group = self.device.create_bind_group(bindGroupDesc)

        return mesh
        #exit()

    def create_shader_module(self):
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, shader_code
        )
        return shader_module
    
    def create_pipeline(self):
        shader_module = self.create_shader_module()

        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X3,
                    offset=kPositionByteOffset,
                    shader_location=0,
                ),
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X2,
                    offset=kUVByteOffset,
                    shader_location=1,
                ),
            ]
        )

        vertBufferLayout = wgpu.VertexBufferLayout(
            array_stride=kVertexDataStride,
            attribute_count=2,
            attributes=vertAttributes[0],
        )

        colorTargetState = wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetState,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=True,
            depth_compare=wgpu.CompareFunction.LESS,
        )

        primitive = wgpu.PrimitiveState(cull_mode=wgpu.CullMode.BACK)

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayout,
        )

        bgl_entries = wgpu.BindGroupLayoutEntries(
            [
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
                wgpu.BindGroupLayoutEntry(
                    binding=2,
                    visibility=wgpu.ShaderStage.VERTEX,
                    buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM)
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

        rp_descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )

        return self.device.create_render_pipeline(rp_descriptor)
