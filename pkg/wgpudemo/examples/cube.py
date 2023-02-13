import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
import math
import glm

from loguru import logger
import glfw
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)

vertex_data = np.array([
        # vec4<f32> position, vec2<f32> uv,
     1, -1,  1,  1,      1, 1,
    -1, -1,  1,  1,      0, 1,
    -1, -1, -1,  1,      0, 0,
     1, -1, -1,  1,      1, 0,
     1, -1,  1,  1,      1, 1,
    -1, -1, -1,  1,      0, 0,

     1,  1,  1,  1,      1, 1,
     1, -1,  1,  1,      0, 1,
     1, -1, -1,  1,      0, 0,
     1,  1, -1,  1,      1, 0,
     1,  1,  1,  1,      1, 1,
     1, -1, -1,  1,      0, 0,

    -1,  1,  1,  1,      1, 1,
     1,  1,  1,  1,      0, 1,
     1,  1, -1,  1,      0, 0,
    -1,  1, -1,  1,      1, 0,
    -1,  1,  1,  1,      1, 1,
     1,  1, -1,  1,      0, 0,

    -1, -1,  1,  1,      1, 1,
    -1,  1,  1,  1,      0, 1,
    -1,  1, -1,  1,      0, 0,
    -1, -1, -1,  1,      1, 0,
    -1, -1,  1,  1,      1, 1,
    -1,  1, -1,  1,      0, 0,

     1,  1,  1,  1,      1, 1,
    -1,  1,  1,  1,      0, 1,
    -1, -1,  1,  1,      0, 0,
    -1, -1,  1,  1,      0, 0,
     1, -1,  1,  1,      1, 0,
     1,  1,  1,  1,      1, 1,

     1, -1, -1,  1,      1, 1,
    -1, -1, -1,  1,      0, 1,
    -1,  1, -1,  1,      0, 0,
     1,  1, -1,  1,      1, 0,
     1, -1, -1,  1,      1, 1,
    -1,  1, -1,  1,      0, 0,
    ],
    dtype=np.float32,
)


shader_code = """
struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@binding(0) @group(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
  @location(1) frag_colour: vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = uniforms.modelViewProjectionMatrix * in.pos;
  let frag_colour = 0.5 * (in.pos + vec4(1));
  return VertexOutput(vert_pos, in.uv, frag_colour);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return in.frag_colour;
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

        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, shader_code
        )

        # Pipeline creation

        # TODO: Need to implement kwargs initializers
        va0 = wgpu.VertexAttribute()
        va0.format = wgpu.VertexFormat.FLOAT32X4
        va0.offset = self.kPositionByteOffset
        va0.shader_location = 0

        va1 = wgpu.VertexAttribute()
        va1.format = wgpu.VertexFormat.FLOAT32X2
        va1.offset = self.kUVByteOffset
        va1.shader_location = 1

        vertAttributes = wgpu.VertexAttributes([va0, va1])

        vertBufferLayout = wgpu.VertexBufferLayout()
        vertBufferLayout.array_stride = self.kCubeDataStride * sizeof(c_float)
        vertBufferLayout.attribute_count = 2
        vertBufferLayout.attributes = vertAttributes[0]

        colorTargetState = wgpu.ColorTargetState()
        colorTargetState.format = wgpu.TextureFormat.BGRA8_UNORM

        fragmentState = wgpu.FragmentState()
        fragmentState.module = shader_module
        fragmentState.entry_point = "fs_main"
        fragmentState.target_count = 1
        fragmentState.targets = colorTargetState

        depthStencilState = wgpu.DepthStencilState()
        depthStencilState.format = wgpu.TextureFormat.DEPTH24_PLUS
        depthStencilState.depth_write_enabled = True
        depthStencilState.depth_compare = wgpu.CompareFunction.LESS

        primitive = wgpu.PrimitiveState()
        primitive.cull_mode = wgpu.CullMode.BACK

        descriptor = wgpu.RenderPipelineDescriptor()
        descriptor.label = "Main Render Pipeline"
        descriptor.vertex.module = shader_module
        descriptor.vertex.entry_point = "vs_main"
        descriptor.vertex.buffer_count = 1
        descriptor.vertex.buffers = vertBufferLayout
        descriptor.primitive = primitive
        descriptor.depth_stencil = depthStencilState
        descriptor.fragment = fragmentState
        self.pipeline = self.device.create_render_pipeline(descriptor)

        # Create depth texture
        extent = wgpu.Extent3D()
        extent.width = self.kWidth
        extent.height = self.kHeight
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            extent,
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

        bindEntry = wgpu.BindGroupEntry()
        bindEntry.binding = 0
        bindEntry.buffer = self.uniformBuffer
        bindEntry.size = self.uniformBufferSize

        bindGroupDesc = wgpu.BindGroupDescriptor()
        bindGroupDesc.label = "Uniform bind group"
        bindGroupDesc.layout = self.pipeline.get_bind_group_layout(0)
        bindGroupDesc.entry_count = 1
        bindGroupDesc.entries = bindEntry

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

        aspect = float(self.kWidth) / float(self.kHeight)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

    @property
    def transform_matrix(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        #print(ms)
        viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 0, -4))
        rotMatrix = glm.rotate(glm.mat4(1.0), math.sin(ms), WORLD_AXIS_X)
        rotMatrix = glm.rotate(rotMatrix, math.cos(ms), WORLD_AXIS_Y)
        return self.projectionMatrix * viewMatrix * rotMatrix

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, vertex_data, wgpu.BufferUsage.VERTEX
        )
        """
        constexpr uint64_t uniformBufferSize = 4 * 16;  // mat4x4<f32>
        auto uniformBuffer = dusk::webgpu::createBuffer(
            device, "Uniform buffer", uniformBufferSize, wgpu::BufferUsage::Uniform);
        """
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device, "Uniform buffer", self.uniformBufferSize, wgpu.BufferUsage.UNIFORM)

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "Hello", None, None)

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

        sd = wgpu.SurfaceDescriptor()
        sd.next_in_chain = wsd

        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor()
        scDesc.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
        scDesc.format = wgpu.TextureFormat.BGRA8_UNORM
        scDesc.width = self.kWidth
        scDesc.height = self.kHeight
        # scDesc.present_mode = wgpu.PresentMode.FIFO
        scDesc.present_mode = wgpu.PresentMode.MAILBOX
        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def render(self, backbufferView: wgpu.TextureView):
        attachment = wgpu.RenderPassColorAttachment()
        attachment.view = backbufferView
        attachment.load_op = wgpu.LoadOp.CLEAR
        attachment.store_op = wgpu.StoreOp.STORE
        attachment.clear_value = wgpu.Color(.5, .5, .5, 1.)

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment()
        depthStencilAttach.view = self.depthTexture.create_view()
        depthStencilAttach.depth_load_op = wgpu.LoadOp.CLEAR
        depthStencilAttach.depth_store_op = wgpu.StoreOp.STORE
        depthStencilAttach.depth_clear_value = 1.0

        renderpass = wgpu.RenderPassDescriptor()
        renderpass.label = "Main Render Pass"
        renderpass.color_attachment_count = 1
        renderpass.color_attachments = attachment
        renderpass.depth_stencil_attachment = depthStencilAttach

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
        self.device.queue.write_buffer(self.uniformBuffer, 0, as_capsule(glm.value_ptr(transform)), self.uniformBufferSize)
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


if __name__ == "__main__":
    HelloWgpu().run()
