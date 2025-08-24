from ctypes import Structure, c_float, sizeof
import time
import math
import glm

from loguru import logger
import numpy as np
import trimesh as tm

from crunge import wgpu
from crunge.wgpu import utils

from crunge.engine import Viewport

from ..demo import Demo

WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)
WORLD_SCALE = 1

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


class Vertex(Structure):
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


class ModelDemo(Demo):
    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    kPositionByteOffset = 0
    kUVByteOffset = 3 * sizeof(c_float)
    kVertexDataStride = 5

    def on_size(self):
        super().on_size()
        self.resize_camera(self.size)

    def resize_camera(self, size: glm.ivec2):
        aspect = float(size.x) / float(size.y)
        # fov_y_radians = (2.0 * math.pi) / 5.0
        fov_y_radians = glm.radians(60.0)
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

    def create_device_objects(self):
        self.create_meshes()
        self.create_buffers()
        self.create_pipeline()

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        # Pipeline creation

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X3,
                offset=self.kPositionByteOffset,
                shader_location=0,
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2,
                offset=self.kUVByteOffset,
                shader_location=1,
            ),
        ]

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=self.kVertexDataStride * sizeof(c_float),
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
            buffers=vertBufferLayouts,
        )

        bgl_entries = [
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
        logger.debug(self.resource_root)
        mesh_path = self.resource_root / "models" / "Fourareen" / "fourareen.gltf"
        scene = tm.load(str(mesh_path))
        geometries = list(scene.geometry.values())
        logger.debug(geometries)
        self.mesh = mesh = geometries[0]
        logger.debug(mesh.__dict__)
        visual = mesh.visual
        logger.debug(mesh.visual.__dict__)
        material = visual.material
        logger.debug(material.__dict__)
        self.create_texture(material)

        # Vertices
        vertices = mesh.vertices.astype(np.float32)
        logger.debug(f"vertices type: {type(vertices)}")
        logger.debug(f"vertices:  {vertices}")
        n_vertices = len(vertices)
        logger.debug(f"n_vertices:  {n_vertices}")

        logger.debug(mesh.visual.__dict__)

        # Texture Coordinates
        uv_coords = mesh.visual.uv.astype(np.float32)

        logger.debug(f"uv_coords type: {type(uv_coords)}")
        logger.debug(f"uv_coords:  {uv_coords}")
        n_uv_coords = len(uv_coords)
        logger.debug(f"n_uv_coords:  {n_uv_coords}")

        # Vertex Data
        vertex_data = self.vertex_data = np.concatenate((vertices, uv_coords), axis=1)
        logger.debug(type(vertex_data))
        logger.debug(f"vertex_data:  {vertex_data}")

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

    def create_texture(self, material):
        image = material.baseColorTexture
        im = None
        logger.debug(f"image mode: {image.mode}")
        if image.mode != "RGBA":
            im = np.array(image.convert("RGBA"))
        else:
            im = np.array(image)
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

        sampler_desc = wgpu.SamplerDescriptor(
            address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,
            mag_filter=wgpu.FilterMode.LINEAR,
            min_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
        )

        self.sampler = self.device.create_sampler(sampler_desc)

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

    def _draw(self):
        viewport = Viewport.get_current()

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.viewport.depth_stencil_texture_view,
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

        super()._draw()

    def frame(self):
        transform = self.transform_matrix
        self.device.queue.write_buffer(self.uniformBuffer, 0, transform)
        super().frame()


def main():
    ModelDemo().run()


if __name__ == "__main__":
    main()
