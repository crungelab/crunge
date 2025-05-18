from enum import IntEnum
from ctypes import Structure, c_float, sizeof
import time
import sys
import math
import glm
from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm
import imageio.v3 as iio

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..common import Demo

resource_root = Path(__file__).parent.parent.parent / "resources"

WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)
WORLD_SCALE = 10


class Binding(IntEnum):
    SAMPLER = 0
    TEXTURE = 1
    UNIFORM = 2


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


kWidth = 1024
kHeight = 768

kPositionByteOffset = Vertex.pos.offset
kUVByteOffset = Vertex.uv.offset
kVertexDataStride = sizeof(Vertex)


class MeshTextureDemo(Demo):
    depth_stencil_view: wgpu.TextureView = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None

    def __init__(self):
        super().__init__()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_meshes()
        self.create_buffers()
        self.create_textures()
        self.create_pipeline()

    def create_depth_stencil_view(self):
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.size.x, self.size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )
        self.depth_stencil_view = self.depthTexture.create_view()

    def create_pipeline(self):
        shader_module = self.create_shader_module(shader_code)

        vertAttributes = [
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

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=kVertexDataStride,
                attributes=vertAttributes,
            )
        ]

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
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
            buffers=vb_layouts,
        )

        bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=Binding.SAMPLER,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=Binding.TEXTURE,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=Binding.UNIFORM,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bgl])

        rp_descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(rp_descriptor)

        view: wgpu.TextureView = self.texture.create_view()

        bg_entries = [
            wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, texture_view=view),
            wgpu.BindGroupEntry(
                binding=2, buffer=self.uniformBuffer, size=self.uniformBufferSize
            ),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture+Uniform bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entries=bg_entries,
        )

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

        aspect = float(kWidth) / float(kHeight)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)
        # exit()

    @property
    def transform_matrix(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        # print(ms)
        viewMatrix = glm.mat4(1.0)
        viewMatrix = glm.translate(viewMatrix, glm.vec3(0, 0, -4))
        viewMatrix = glm.scale(
            viewMatrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE)
        )

        rotMatrix = glm.mat4(1.0)
        rotMatrix = glm.rotate(rotMatrix, math.sin(ms), WORLD_AXIS_X)
        rotMatrix = glm.rotate(rotMatrix, math.cos(ms), WORLD_AXIS_Y)
        return self.projectionMatrix * viewMatrix * rotMatrix

    def create_meshes(self):
        mesh_path = resource_root / "models" / "Fuze" / "fuze.obj"
        self.mesh = mesh = tm.load(str(mesh_path))
        # Vertices
        vertices = self.vertex_data = mesh.vertices.astype(np.float32)
        logger.debug(f"vertices type: {type(vertices)}")
        logger.debug(f"vertices:  {vertices}")
        n_vertices = len(vertices)
        logger.debug(f"n_vertices:  {n_vertices}")

        uv_coords = mesh.visual.uv.astype(np.float32)
        logger.debug(f"uv_coords type: {type(uv_coords)}")
        logger.debug(f"uv_coords:  {uv_coords}")
        n_uv_coords = len(uv_coords)
        logger.debug(f"n_uv_coords:  {n_uv_coords}")

        vertex_data = self.vertex_data = np.concatenate((vertices, uv_coords), axis=1)
        # logger.debug(type(vertex_data))
        logger.debug(f"vertex_data:  {vertex_data}")
        # exit()

        # Indices
        indices = self.index_data = self.mesh.faces.astype(np.uint32)
        logger.debug(f"indices:  {indices}")
        n_indices = self.n_indices = len(indices)
        logger.debug(f"n_indices:  {n_indices}")
        # exit()

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", self.vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", self.index_data, wgpu.BufferUsage.INDEX
        )
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_textures(self):
        path = resource_root / "models" / "Fuze" / "fuze_uv.jpg"
        im = iio.imread(
            path,
            plugin="pillow",
            mode="RGBA",
        )
        shape = im.shape
        logger.debug(shape)
        im_width = shape[0]
        im_height = shape[1]
        im_depth = 1

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()

        bytes_per_row = 4 * im_width
        logger.debug(bytes_per_row)
        rows_per_image = im_height

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            im,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            # The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

    def render(self, view: wgpu.TextureView):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_stencil_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.uniformBindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(len(self.index_data) * 3)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

    def frame(self):
        transform = self.transform_matrix

        self.device.queue.write_buffer(self.uniformBuffer, 0, transform)

        backbufferView: wgpu.TextureView = self.get_surface_view()
        backbufferView.set_label("Back Buffer Texture View")
        self.render(backbufferView)
        self.surface.present()


def main():
    MeshTextureDemo().run()


if __name__ == "__main__":
    main()
