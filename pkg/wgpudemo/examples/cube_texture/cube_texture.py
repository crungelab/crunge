import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
import math
import glm
from pathlib import Path

from loguru import logger
import glfw
import numpy as np
import imageio.v3 as iio

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from data import vertex_data

WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)

vs_shader_code = """
@vertex fn main(@location(0) pos : vec4<f32>) -> @builtin(position) vec4<f32> {
    return pos;
}
"""

fs_shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture : texture_2d<f32>;

@fragment fn main(@builtin(position) FragCoord : vec4<f32>)
                        -> @location(0) vec4<f32> {
    return textureSample(myTexture, mySampler, FragCoord.xy / vec2<f32>(800.0, 600.0));
    //return textureSample(myTexture, mySampler, FragCoord.xy);
}
"""

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
  return textureSample(myTexture, mySampler, in.uv);
}
"""
#
"""
@fragment fn main(@builtin(position) FragCoord : vec4<f32>)
                        -> @location(0) vec4<f32> {
    return textureSample(myTexture, mySampler, FragCoord.xy / vec2<f32>(800.0, 600.0));
    //return textureSample(myTexture, mySampler, FragCoord.xy);
}
"""

class HelloWgpu:
    device: wgpu.Device = None
    queue: wgpu.Queue = None
    readbackBuffer: wgpu.Buffer = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None
    swap_chain: wgpu.SwapChain = None
    depth_stencil_view: wgpu.TextureView = None

    vertex_buffer: wgpu.Buffer = None

    kWidth = 1024
    kHeight = 768

    kVertexCount = 36
    kPositionByteOffset = 0
    kUVByteOffset = 4 * sizeof(c_float)
    kCubeDataStride = 6

    def __init__(self):
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.set_label("Primary Device")
        self.device.enable_logging()
        self.queue = self.device.get_queue()

        self.create_buffers()
        self.create_textures()

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, shader_code
        )

        # Pipeline creation

        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X4,
                    offset=self.kPositionByteOffset,
                    shader_location=0,
                ),
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X2,
                    offset=self.kUVByteOffset,
                    shader_location=1,
                ),
            ]
        )

        vertBufferLayout = wgpu.VertexBufferLayout(
            array_stride=self.kCubeDataStride * sizeof(c_float),
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

        self.pipeline = self.device.create_render_pipeline(rp_descriptor)

        # Create depth texture
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.kWidth, self.kHeight),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

        view: wgpu.TextureView = self.texture.create_view()

        bg_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=view),
                wgpu.BindGroupEntry(binding=2, buffer=self.uniformBuffer, size=self.uniformBufferSize),
            ]
        )

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture+Uniform bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=len(bg_entries),
            entries=bg_entries[0],
        )

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

        aspect = float(self.kWidth) / float(self.kHeight)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)
        #exit()

    @property
    def transform_matrix(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        # print(ms)
        viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 0, -4))
        rotMatrix = glm.rotate(glm.mat4(1.0), math.sin(ms), WORLD_AXIS_X)
        rotMatrix = glm.rotate(rotMatrix, math.cos(ms), WORLD_AXIS_Y)
        return self.projectionMatrix * viewMatrix * rotMatrix

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_textures(self):
        path = Path(__file__).parent.parent / "resources" / "textures" / "python_logo.png"
        im = iio.imread(path)
        shape = im.shape
        logger.debug(shape)
        im_width = shape[0]
        im_height = shape[1]
        #im_depth = shape[2]
        im_depth = 1
        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        #size = im.nbytes
        logger.debug(size)

        descriptor = wgpu.TextureDescriptor(
            dimension = wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count = 1,
            format = wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count = 1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()
        
        bytes_per_row = 4 * im_width
        logger.debug(bytes_per_row)
        rows_per_image = im_height

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.ImageCopyTexture(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            utils.as_capsule(im),
            # Data size
            size,
            # The layout of the texture
            wgpu.TextureDataLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            #The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

        """
        data = im
        staging_buffer = utils.create_buffer_from_ndarray(
            self.device, data, wgpu.BufferUsage.COPY_SRC
        )
    
        image_copy_buffer = utils.create_image_copy_buffer(staging_buffer, 0, bytes_per_row, rows_per_image)
        image_copy_texture = utils.create_image_copy_texture(self.texture)
        copy_size = wgpu.Extent3D(im_width, im_height, im_depth)

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        encoder.copy_buffer_to_texture(image_copy_buffer, image_copy_texture, copy_size)

        copy: wgpu.CommandBuffer = encoder.finish()
        self.queue.submit(1, copy)
        """

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "Cube", None, None)

    def create_swapchain(self):
        handle, display = None, None

        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            handle = glfw.get_win32_window(self.window)
        elif sys.platform == "linux":
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()

        logger.debug(handle)

        nwh = as_capsule(handle)
        logger.debug(nwh)

        wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
        wsd.hwnd = nwh
        wsd.hinstance = None

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            width=self.kWidth,
            height=self.kHeight,
            present_mode=wgpu.PresentMode.MAILBOX,
        )

        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def render(self, view: wgpu.TextureView):
        attachment = wgpu.RenderPassColorAttachment(
            view=view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depthTexture.create_view(),
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=attachment,
            depth_stencil_attachment=depthStencilAttach,
        )

        commands = wgpu.CommandBuffer()
        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.uniformBindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(self.kVertexCount)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

    def frame(self):
        transform = self.transform_matrix
        self.device.queue.write_buffer(
            self.uniformBuffer,
            0,
            as_capsule(glm.value_ptr(transform)),
            self.uniformBufferSize,
        )
        backbufferView: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        backbufferView.set_label("Back Buffer Texture View")
        self.render(backbufferView)
        self.swap_chain.present()

    def run(self):
        self.create_window()
        self.create_swapchain()

        last_time = None
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.frame()

        glfw.destroy_window(self.window)
        glfw.terminate()


def main():
    HelloWgpu().run()

if __name__ == "__main__":
    main()
