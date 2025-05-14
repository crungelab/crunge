import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys

from loguru import logger
import numpy as np
import glm

from crunge.core import as_capsule

from crunge import sdl
from crunge import wgpu
from crunge import imgui

import crunge.wgpu.utils as utils
from crunge.engine import Renderer

from ..demo import Demo

from .uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    Uniforms,
)

"""
struct ImDrawVert
{
    ImVec2  pos;
    ImVec2  uv;
    ImU32   col;
};
#else
// You can override the vertex format layout by defining IMGUI_OVERRIDE_DRAWVERT_STRUCT_LAYOUT in imconfig.h
// The code expect ImVec2 pos (8 bytes), ImVec2 uv (8 bytes), ImU32 col (4 bytes)
"""


class ImDrawVert(Structure):
    _fields_ = [
        ("pos", c_float * 2),
        ("uv", c_float * 2),
        ("col", c_uint32),
    ]


vs_shader_code = """
struct VertexInput {
    @location(0) position: vec2<f32>,
    @location(1) uv: vec2<f32>,
    @location(2) color: vec4<f32>,
};

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) uv: vec2<f32>,
};

struct Uniforms {
    mvp: mat4x4<f32>,
    gamma: f32,
};

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

@vertex
fn main(in: VertexInput) -> VertexOutput {
    var out: VertexOutput;
    out.position = uniforms.mvp * vec4<f32>(in.position, 0.0, 1.0);
    out.color = in.color;
    out.uv = in.uv;
    return out;
}
"""

fs_shader_code = """
struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) color: vec4<f32>,
    @location(1) uv: vec2<f32>,
};

struct Uniforms {
    mvp: mat4x4<f32>,
    gamma: f32,
};

@group(0) @binding(0) var<uniform> uniforms: Uniforms;
@group(0) @binding(1) var s: sampler;
@group(0) @binding(2) var t: texture_2d<f32>;

@fragment
fn main(in: VertexOutput) -> @location(0) vec4<f32> {
    let color = in.color * textureSample(t, s, in.uv);
    let corrected_color = pow(color.rgb, vec3<f32>(uniforms.gamma));
    return vec4<f32>(corrected_color, color.a);
}
"""


def compute_framebuffer_scale(window_size, frame_buffer_size):
    win_width, win_height = window_size
    fb_width, fb_height = frame_buffer_size

    if win_width != 0 and win_width != 0:
        return fb_width / win_width, fb_height / win_height

    return 1.0, 1.0


class WImGuiDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    texture_view: wgpu.TextureView = None
    sampler: wgpu.Sampler = None

    def __init__(self):
        super().__init__()

        self.last_mouse = glm.vec2(-sys.float_info.max, -sys.float_info.max)

        self.imgui_context = imgui.create_context()
        imgui.set_current_context(self.imgui_context)

        imgui.style_colors_dark()

        io = imgui.get_io()
        self.io = io

    def _set_pixel_ratio(self):
        window_size = sdl.get_window_size(self.window)
        self.io.display_size = window_size

        framebuffer_size = sdl.get_window_size_in_pixels(self.window)
        pixel_ratio = compute_framebuffer_scale(window_size, framebuffer_size)
        self.io.display_framebuffer_scale = pixel_ratio

    def create_device_objects(self):
        self.create_buffers()
        self.create_textures()
        self.create_pipeline()

    def create_window(self):
        super().create_window()
        self._set_pixel_ratio()

    def on_mouse_enter(self, event: sdl.WindowEvent):
        super().on_mouse_enter(event)
        self.io.add_mouse_pos_event(self.last_mouse.x, self.last_mouse.y)

    def on_mouse_leave(self, event: sdl.WindowEvent):
        super().on_mouse_leave(event)
        last_mouse = self.io.mouse_pos
        self.last_mouse = glm.vec2(last_mouse[0], last_mouse[1])
        self.io.add_mouse_pos_event(-sys.float_info.max, -sys.float_info.max)

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        logger.debug(f"on_mouse_motion: {event}")
        super().on_mouse_motion(event)
        x, y = event.x, event.y
        self.io.add_mouse_pos_event(x, y)
        self.last_mouse = glm.vec2(x, y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        button = event.button - 1  # SDL starts at 1, ImGui starts at 0
        if button < 3:
            self.io.add_mouse_button_event(button, event.down)

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        x, y = event.x, event.y
        self.io.add_mouse_wheel_event(x, y)

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer(
            self.device, "VERTEX", imgui.VERTEX_SIZE * 65536, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer(
            self.device, "INDEX", imgui.INDEX_SIZE * 65536, wgpu.BufferUsage.INDEX
        )

        self.uniform_buffer_size = sizeof(Uniforms)
        self.uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_textures(self):
        io = self.io
        pixels, width, height, bpp = io.fonts.get_tex_data_as_rgba32()
        logger.debug(f"width: {width}")
        logger.debug(f"height: {height}")
        logger.debug(f"bpp: {bpp}")

        texture_desc = wgpu.TextureDescriptor(
            label="Dear ImGui Font Texture",
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(width, height, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )
        self.texture = self.device.create_texture(texture_desc)

        texture_view_desc = wgpu.TextureViewDescriptor(
            format=wgpu.TextureFormat.RGBA8_UNORM,
            dimension=wgpu.TextureViewDimension.E2D,
            base_mip_level=0,
            mip_level_count=1,
            base_array_layer=0,
            array_layer_count=1,
            aspect=wgpu.TextureAspect.ALL,
        )

        self.texture_view = self.texture.create_view(texture_view_desc)

        '''
        sampler_desc = wgpu.SamplerDescriptor(
            min_filter=wgpu.FilterMode.LINEAR,
            mag_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,
            max_anisotropy=1,
        )
        '''
        sampler_desc = wgpu.SamplerDescriptor()

        self.sampler = self.device.create_sampler(sampler_desc)

        # size = utils.divround_up(pixels.nbytes, 256)
        # size = utils.divround_up(width * height * bpp, 256)
        size = width * height * bpp

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            pixels,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=width * bpp,
                rows_per_image=height,
            ),
            # The texture size
            wgpu.Extent3D(width, height, 1),
        )

        '''
        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            utils.as_capsule(pixels),
            # Data size
            # width * height * bpp,
            size,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=width * bpp,
                rows_per_image=height,
            ),
            # The texture size
            wgpu.Extent3D(width, height, 1),
        )
        '''

        # io.fonts.set_tex_id(id(self.texture_view))
        # io.fonts.clear_tex_data()

    def create_pipeline(self):
        logger.debug("create_pipeline")

        vs_module = self.gfx.create_shader_module(vs_shader_code)
        fs_module = self.gfx.create_shader_module(fs_shader_code)

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2,
                offset=ImDrawVert.uv.offset,
                shader_location=1,
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.UNORM8X4,
                offset=ImDrawVert.col.offset,
                shader_location=2,
            ),
        ]

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=sizeof(ImDrawVert),
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
            module=fs_module,
            entry_point="main",
            target_count=1,
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="main",
            buffer_count=1,
            buffers=vb_layouts,
        )

        bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
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

        bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(bgl_entries), entries=bgl_entries
        )
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=[bgl]
        )

        primitive = wgpu.PrimitiveState(
            topology=wgpu.PrimitiveTopology.TRIANGLE_LIST,
            strip_index_format=wgpu.IndexFormat.UNDEFINED,
            front_face=wgpu.FrontFace.CW,
            cull_mode=wgpu.CullMode.NONE,
        )

        # TODO: depth_stencil_state
        """
        depth_stencil_state = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS_STENCIL8,
            depth_write_enabled=False,
            depth_compare=wgpu.CompareFunction.ALWAYS,
            stencil_front=wgpu.StencilFaceState(
                compare=wgpu.CompareFunction.ALWAYS,
            ),
            stencil_back=wgpu.StencilFaceState(
                compare=wgpu.CompareFunction.ALWAYS,
            ),
        )
        """

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            # depth_stencil=depth_stencil_state,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0, buffer=self.uniform_buffer, size=self.uniform_buffer_size
            ),
            wgpu.BindGroupEntry(binding=1, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=2, texture_view=self.texture_view),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.bindGroup = self.device.create_bind_group(bindGroupDesc)

    def render_draw_data(
        self, draw_data: imgui.DrawData, pass_enc: wgpu.RenderPassEncoder
    ):
        # logger.debug("render_draw_data")
        vtx_offset = 0
        idx_offset = 0
        for commands in draw_data.cmd_lists:
            # logger.debug('write vertex_buffer')
            utils.write_buffer(
                self.device,
                self.vertex_buffer,
                vtx_offset * imgui.VERTEX_SIZE,
                commands.vtx_buffer_data,
                #commands.vtx_buffer_size * imgui.VERTEX_SIZE,
            )
            # logger.debug('write index_buffer')
            utils.write_buffer(
                self.device,
                self.index_buffer,
                idx_offset * imgui.INDEX_SIZE,
                commands.idx_buffer_data,
                #commands.idx_buffer_size * imgui.INDEX_SIZE,
            )

            for command in commands:
                if command.user_callback:
                    command.user_callback(
                        self, draw_data, commands, command, command.user_callback_data
                    )
                else:
                    """
                    wgpuRenderPassEncoderSetScissorRect(pass_encoder, (uint32_t)clip_min.x, (uint32_t)clip_min.y, (uint32_t)(clip_max.x - clip_min.x), (uint32_t)(clip_max.y - clip_min.y));
                    wgpuRenderPassEncoderDrawIndexed(pass_encoder, pcmd->ElemCount, 1, pcmd->IdxOffset + global_idx_offset, pcmd->VtxOffset + global_vtx_offset, 0);
                    """
                    pass_enc.set_scissor_rect(
                        int(command.clip_rect[0]),
                        int(command.clip_rect[1]),
                        int(command.clip_rect[2] - command.clip_rect[0]),
                        int(command.clip_rect[3] - command.clip_rect[1]),
                    )
                    pass_enc.draw_indexed(
                        command.elem_count,
                        1,
                        command.idx_offset + idx_offset,
                        command.vtx_offset + vtx_offset,
                        0,
                    )

            vtx_offset += commands.vtx_buffer_size
            idx_offset += commands.idx_buffer_size

    def pre_draw(self, renderer: Renderer):
        imgui.new_frame()

    def draw(self, renderer: Renderer):
        # logger.debug("draw")
        self.draw_buttons()
        self.draw_more_buttons()
        imgui.show_demo_window()

        super().draw(renderer)

    def post_draw(self, renderer: Renderer):
        # logger.debug("render")
        imgui.end_frame()
        imgui.render()
        io = imgui.get_io()
        draw_data = imgui.get_draw_data()

        display_width, display_height = io.display_size
        fb_scale = io.display_framebuffer_scale
        fb_width = int(display_width * fb_scale[0])
        fb_height = int(display_height * fb_scale[1])
        if fb_width == 0 or fb_height == 0:
            return

        # def ortho(left: glm_typing.Number, right: glm_typing.Number, bottom: glm_typing.Number, top: glm_typing.Number, zNear: glm_typing.Number, zFar: glm_typing.Number, /) -> mat4x4: ...
        mvp = glm.ortho(0.0, display_width, display_height, 0.0, -1.0, 1.0)

        uniforms = Uniforms()
        uniforms.mvp.data = cast_matrix4(mvp)
        uniforms.gamma = 1.0

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            uniforms
        )

        '''
        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(uniforms),
            self.uniform_buffer_size,
        )
        '''

        draw_data.scale_clip_rects(fb_scale)

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                #view=renderer.texture_view,
                view = renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        self.render_draw_data(draw_data, pass_enc)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        super().post_draw(renderer)

    def draw_buttons(self):
        imgui.begin("Buttons")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()

    def draw_more_buttons(self):
        imgui.begin("More Buttons")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()


def main():
    WImGuiDemo().create().run()


if __name__ == "__main__":
    main()
