from ctypes import Structure, c_float, c_uint32, sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import imgui

from ..renderer import Renderer
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture2D
from ..resource.sampler import Sampler
from ..vu import Vu

from .uniforms import (
    cast_matrix4,
    Uniforms,
)


class ImDrawVert(Structure):
    _fields_ = [
        ("pos", c_float * 2),
        ("uv",  c_float * 2),
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
    let c = in.color * textureSample(t, s, in.uv);
    let rgb = pow(c.rgb, vec3<f32>(uniforms.gamma));
    return vec4<f32>(rgb, c.a);
}
"""


@klass.singleton
class ImGuiSampler(Sampler):
    def __init__(self) -> None:

        sampler_desc = wgpu.SamplerDescriptor(
            min_filter=wgpu.FilterMode.LINEAR,
            mag_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_w=wgpu.AddressMode.CLAMP_TO_EDGE,
            max_anisotropy=1,
        )

        sampler = self.device.create_sampler(sampler_desc)

        super().__init__(sampler)

@klass.singleton_producer
class ImGuiVu(Vu):
    def __init__(self) -> None:
        super().__init__()
        self.io = imgui.get_io()
        # Opt-in: renderer manages textures (dynamic fonts etc.)
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_TEXTURES
        self.io.backend_flags |= imgui.BackendFlags.RENDERER_HAS_VTX_OFFSET

        self.sampler = ImGuiSampler()
        self.image_bind_groups = {}  # cache: key = TextureId (WGPUTextureView or your id)

    def _create(self):
        super()._create()
        self.create_device_objects()

    def create_device_objects(self):
        self.create_buffers()
        # NOTE: do NOT build/upload font atlas here anymore (ImGui 1.92+)
        self.create_pipeline()

    def create_buffers(self):
        logger.debug("create_buffers")
        self.vertex_buffer = utils.create_buffer(
            self.device, "VERTEX", imgui.VERTEX_SIZE * 65536, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer(
            self.device, "INDEX", imgui.INDEX_SIZE * 131072, wgpu.BufferUsage.INDEX
        )
        self.uniform_buffer_size = sizeof(Uniforms)
        self.uniform_buffer = utils.create_buffer(
            self.device, "Uniform buffer", self.uniform_buffer_size, wgpu.BufferUsage.UNIFORM
        )

    def create_pipeline(self):
        logger.debug("create_pipeline")
        vs_module = self.gfx.create_shader_module(vs_shader_code)
        fs_module = self.gfx.create_shader_module(fs_shader_code)

        vertex_attributes = [
            wgpu.VertexAttribute(format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0),
            wgpu.VertexAttribute(format=wgpu.VertexFormat.FLOAT32X2, offset=ImDrawVert.uv.offset,  shader_location=1),
            wgpu.VertexAttribute(format=wgpu.VertexFormat.UNORM8X4,  offset=ImDrawVert.col.offset, shader_location=2),
        ]
        vertex_buffer_layouts = [
            wgpu.VertexBufferLayout(array_stride=sizeof(ImDrawVert), attributes=vertex_attributes)
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
            wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM, blend=blend_state, write_mask=wgpu.ColorWriteMask.ALL)
        ]

        fragment_state = wgpu.FragmentState(module=fs_module, entry_point="main", targets=color_targets)
        vertex_state   = wgpu.VertexState(module=vs_module, entry_point="main", buffers=vertex_buffer_layouts)

        bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(type=wgpu.SamplerBindingType.FILTERING),
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

        bgl = self.device.create_bind_group_layout(wgpu.BindGroupLayoutDescriptor(entries=bgl_entries))
        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bgl])

        primitive = wgpu.PrimitiveState(
            topology=wgpu.PrimitiveTopology.TRIANGLE_LIST,
            strip_index_format=wgpu.IndexFormat.UNDEFINED,
            front_face=wgpu.FrontFace.CW,
            cull_mode=wgpu.CullMode.NONE,
        )

        self.pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="ImGui Render Pipeline",
                layout=self.device.create_pipeline_layout(pl_desc),
                vertex=vertex_state,
                primitive=primitive,
                fragment=fragment_state,
            )
        )

        # Common (uniform+sampler) bindgroup; texture view is provided per draw.
        self.common_bind_group_prefix = [
            wgpu.BindGroupEntry(binding=0, buffer=self.uniform_buffer, size=self.uniform_buffer_size),
            wgpu.BindGroupEntry(binding=1, sampler=self.sampler.sampler),
        ]
        logger.debug("create_pipeline done")


    def update_texture(self, tex: imgui.TextureData):
        status = tex.status
        texture = None

        if status == imgui.WANT_CREATE:
            pixels = tex.pixels  # bytes-like
            width  = tex.width
            height = tex.height
            bpp = tex.bytes_per_pixel

            # Create GPU texture
            texture_desc = wgpu.TextureDescriptor(
                label="Dear ImGui Texture",
                dimension=wgpu.TextureDimension.E2D,
                size=wgpu.Extent3D(width, height, 1),
                sample_count=1,
                format=wgpu.TextureFormat.RGBA8_UNORM,
                mip_level_count=1,
                usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
            )

            wgpu_texture = self.device.create_texture(texture_desc)
            texture = Texture2D(wgpu_texture, glm.ivec2(width, height))
            ResourceManager().add(texture)
            logger.debug(f"ImGuiVu: created dynamic texture id={texture.id} size=({width}x{height})")

            self.queue.write_texture(
                # Tells wgpu where to copy the pixel data
                wgpu.TexelCopyTextureInfo(
                    texture=texture.texture,
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



            # Assign the texture view as ImGui's TextureId
            tex.set_tex_id(texture.id)
            tex.set_status(imgui.TextureStatus.OK)

        if status == imgui.TextureStatus.WANT_DESTROY:
            # The tex.tex_id is a TextureView we created before.
            try:
                view = tex.tex_id  # likely a WGPUTextureView handle
                if view:
                    # If your binding needs explicit release, do it here.
                    # e.g., self.device.release_texture_view(view)  # adapt if needed
                    pass
            except Exception:
                pass
            tex.set_tex_id(imgui.TextureId.INVALID)
            tex.set_status(imgui.TextureStatus.DESTROYED)
            tex.backend_user_data = None
            # Purge any cached bindgroup keyed by this id
            self.image_bind_groups.pop(view, None)

        
    def _update_imgui_textures(self, draw_data: imgui.DrawData):
        #logger.debug("_update_imgui_textures")
        textures_list = draw_data.textures
        if not textures_list:
            return

        for tex in textures_list:
            status = tex.status  # WantCreate / WantUpdate / WantDestroy / OK
            if status == imgui.TextureStatus.OK:
                continue

            if status == imgui.TextureStatus.WANT_DESTROY:
                # The tex.tex_id is a TextureView we created before.
                try:
                    view = tex.tex_id  # likely a WGPUTextureView handle
                    if view:
                        # If your binding needs explicit release, do it here.
                        # e.g., self.device.release_texture_view(view)  # adapt if needed
                        pass
                except Exception:
                    pass
                tex.set_tex_id(imgui.TextureId.INVALID)
                tex.set_status(imgui.TextureStatus.DESTROYED)
                tex.backend_user_data = None
                # Purge any cached bindgroup keyed by this id
                self.image_bind_groups.pop(view, None)
                continue

            # For WANT_CREATE / WANT_UPDATE we (re)upload pixels into a fresh GPU texture
            # Expecting RGBA32 pixels according to 1.92 protocol
            pixels = tex.pixels  # bytes-like
            width  = tex.width
            height = tex.height
            bpp = tex.bytes_per_pixel

            # Create GPU texture
            texture_desc = wgpu.TextureDescriptor(
                label="Dear ImGui Texture",
                dimension=wgpu.TextureDimension.E2D,
                size=wgpu.Extent3D(width, height, 1),
                sample_count=1,
                format=wgpu.TextureFormat.RGBA8_UNORM,
                mip_level_count=1,
                usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
            )

            wgpu_texture = self.device.create_texture(texture_desc)
            texture = Texture2D(wgpu_texture, glm.ivec2(width, height))
            ResourceManager().add(texture)
            logger.debug(f"ImGuiVu: created dynamic texture id={texture.id} size=({width}x{height})")

            self.queue.write_texture(
                # Tells wgpu where to copy the pixel data
                wgpu.TexelCopyTextureInfo(
                    texture=texture.texture,
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



            # Assign the texture view as ImGui's TextureId
            tex.set_tex_id(texture.id)
            tex.set_status(imgui.TextureStatus.OK)
            # Optionally keep GPU handles in backend_user_data if you need to release them later
            #tex.backend_user_data = {"texture": texture, "view": texture.view}

    # --------------------------------------------------------------------------

    def create_image_bind_group(self, tex_id):
        # logger.debug("create_image_bind_group")
        texture = ResourceManager().texture_kit.get(tex_id)
        bindgroup_entries = [
            wgpu.BindGroupEntry(
                binding=0, buffer=self.uniform_buffer, size=self.uniform_buffer_size
            ),
            # wgpu.BindGroupEntry(binding=1, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, sampler=self.sampler.sampler),
            wgpu.BindGroupEntry(binding=2, texture_view=texture.view),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entries=bindgroup_entries,
        )

        return self.device.create_bind_group(bindGroupDesc)

    '''
    def _bind_group_for_tex_id(self, tex_id):
        """
        Make a bindgroup for either:
        - your own engine texture id (found via ResourceManager), or
        - a raw WGPUTextureView produced by ImGui (fonts/dynamic textures).
        """
        logger.debug(f"_bind_group_for_tex_id: {tex_id}")
        # Cached?
        bg = self.image_bind_groups.get(tex_id)
        if bg is not None:
            return bg

        texture_view = None

        # Case 1: your engine-managed images (via ResourceManager)
        texture = ResourceManager().texture_kit.get(tex_id)
        if texture is not None:
            texture_view = texture.view

        # Case 2: ImGui-provided (font/dynamic) texture views
        if texture is None:
            # If your binding surfaces WGPUTextureView objects directly, we can use them.
            # If it returns an int handle, you’ll need a small wrapper here to turn it into a TextureView object.
            texture_view = tex_id  # assume already a WGPUTextureView-compatible object

        bindgroup_entries = list(self.common_bind_group_prefix) + [
            wgpu.BindGroupEntry(binding=2, texture_view=texture_view)
        ]

        bg = self.device.create_bind_group(
            wgpu.BindGroupDescriptor(
                label="ImGui Texture bind group",
                layout=self.pipeline.get_bind_group_layout(0),
                entries=bindgroup_entries,
            )
        )
        self.image_bind_groups[tex_id] = bg
        return bg
    '''

    def render_draw_data(self, draw_data: imgui.DrawData, pass_enc: wgpu.RenderPassEncoder):
        sc_width  = self.wnd.width
        sc_height = self.wnd.height
        fb_width  = draw_data.display_size[0] * draw_data.framebuffer_scale[0]
        fb_height = draw_data.display_size[1] * draw_data.framebuffer_scale[1]
        if fb_width <= 0 or fb_height <= 0:
            return

        for tex in draw_data.textures:
            if tex.status != imgui.TextureStatus.OK:
                self.update_texture(tex)

        clip_pos   = glm.vec2(draw_data.display_pos[0], draw_data.display_pos[1])
        clip_scale = glm.vec2(draw_data.framebuffer_scale[0], draw_data.framebuffer_scale[1])

        vtx_offset = 0
        idx_offset = 0

        for commands in draw_data.cmd_lists:
            utils.write_buffer(self.device, self.vertex_buffer, vtx_offset * imgui.VERTEX_SIZE, commands.vtx_buffer_data)
            utils.write_buffer(self.device, self.index_buffer,  idx_offset * imgui.INDEX_SIZE,  commands.idx_buffer_data)

            for command in commands:
                if command.user_callback:
                    command.user_callback(commands, command)
                    continue

                # Per-draw texture bind (font or user image)
                tex_id = command.tex_ref.id
                
                #bind_group = self._bind_group_for_tex_id(tex_id)
                bind_group = self.image_bind_groups.get(tex_id)
                if bind_group is None:
                    bind_group = self.create_image_bind_group(tex_id)
                    self.image_bind_groups[tex_id] = bind_group

                pass_enc.set_bind_group(0, bind_group)

                # Scissor
                cr = command.clip_rect
                clip_min = glm.vec2((cr[0] - clip_pos.x) * clip_scale.x, (cr[1] - clip_pos.y) * clip_scale.y)
                clip_max = glm.vec2((cr[2] - clip_pos.x) * clip_scale.x, (cr[3] - clip_pos.y) * clip_scale.y)
                if clip_max.x <= clip_min.x or clip_max.y <= clip_min.y:
                    continue

                clip_min.x = max(0, int(clip_min.x))
                clip_min.y = max(0, int(clip_min.y))
                clip_max.x = min(sc_width,  int(clip_max.x))
                clip_max.y = min(sc_height, int(clip_max.y))

                pass_enc.set_scissor_rect(int(clip_min.x), int(clip_min.y),
                                          int(clip_max.x - clip_min.x), int(clip_max.y - clip_min.y))

                pass_enc.draw_indexed(
                    command.elem_count, 1,
                    command.idx_offset + idx_offset,
                    command.vtx_offset + vtx_offset,
                    0,
                )

            vtx_offset += commands.vtx_buffer_size
            idx_offset += commands.idx_buffer_size

    def render(self):
        imgui.render()
        io = imgui.get_io()
        draw_data = imgui.get_draw_data()

        display_width, display_height = io.display_size
        fb_scale = io.display_framebuffer_scale
        fb_width  = int(display_width  * fb_scale[0])
        fb_height = int(display_height * fb_scale[1])
        if fb_width == 0 or fb_height == 0:
            return

        # Update dynamic textures for 1.92:
        #self._update_imgui_textures(draw_data)

        mvp = glm.ortho(0.0, display_width, display_height, 0.0, -1.0, 1.0)

        uniforms = Uniforms()
        uniforms.mvp.data = cast_matrix4(mvp)
        uniforms.gamma = 1.0
        self.device.queue.write_buffer(self.uniform_buffer, 0, uniforms)
        draw_data.scale_clip_rects(fb_scale)

        renderer = Renderer.get_current()
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.LOAD,
                store_op=wgpu.StoreOp.STORE,
            )
        ]
        renderpass = wgpu.RenderPassDescriptor(label="ImGui Render Pass", color_attachments=color_attachments)

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)

        self.render_draw_data(draw_data, pass_enc)

        pass_enc.end()
        self.queue.submit([encoder.finish()])
