from ctypes import Structure, c_float, c_uint32, sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import imgui

from ..composition import Composition
from ..renderer import Renderer
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture2D
from ..resource.sampler import Sampler
from ..vu import Vu

from .uniforms import (
    cast_matrix4,
    Uniforms,
)


# ImTextureID_Invalid is a #define in imgui.h -- ((ImTextureID)0) -- so cxbind
# does not emit it as an attribute. The value is stable across ImGui versions.
TEXTURE_ID_INVALID = 0

# Initial capacities. Both grow on demand.
INITIAL_VERTEX_COUNT = 65536
INITIAL_INDEX_COUNT = 131072

# WebGPU requires queue.writeBuffer offsets and sizes to be 4-byte multiples.
COPY_ALIGNMENT = 4


class ImDrawVert(Structure):
    _fields_ = [
        ("pos", c_float * 2),
        ("uv",  c_float * 2),
        ("col", c_uint32),
    ]


def _align_up(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


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

        # tex_id (int) -> wgpu.BindGroup
        self.image_bind_groups: dict[int, wgpu.BindGroup] = {}

        self.vertex_buffer = None
        self.vertex_capacity = 0
        self.index_buffer = None
        self.index_capacity = 0

        # ImGui's ImDrawIdx is 16-bit by default; honour whatever the binding
        # reports rather than assuming.
        if imgui.INDEX_SIZE == 2:
            self.index_format = wgpu.IndexFormat.UINT16
        elif imgui.INDEX_SIZE == 4:
            self.index_format = wgpu.IndexFormat.UINT32
        else:
            raise RuntimeError(f"Unsupported ImGui index size: {imgui.INDEX_SIZE}")

        if sizeof(ImDrawVert) != imgui.VERTEX_SIZE:
            raise RuntimeError(
                f"ImDrawVert layout mismatch: ctypes says {sizeof(ImDrawVert)}, "
                f"ImGui says {imgui.VERTEX_SIZE}"
            )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def _create(self):
        super()._create()
        self.create_device_objects()

    def create_device_objects(self):
        self.create_buffers()
        self.create_pipeline()

    def create_buffers(self):
        logger.debug("create_buffers")
        self.grow_vertex_buffer(INITIAL_VERTEX_COUNT * imgui.VERTEX_SIZE)
        self.grow_index_buffer(INITIAL_INDEX_COUNT * imgui.INDEX_SIZE)

        self.uniform_buffer_size = sizeof(Uniforms)
        self.uniform_buffer = utils.create_buffer(
            self.device, "ImGui Uniform Buffer", self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def grow_vertex_buffer(self, needed: int) -> None:
        if needed <= self.vertex_capacity:
            return
        capacity = _align_up(max(needed, self.vertex_capacity * 2), 4096)
        logger.debug(f"growing ImGui vertex buffer: {self.vertex_capacity} -> {capacity}")
        self.vertex_buffer = utils.create_buffer(
            self.device, "ImGui Vertex Buffer", capacity, wgpu.BufferUsage.VERTEX
        )
        self.vertex_capacity = capacity

    def grow_index_buffer(self, needed: int) -> None:
        if needed <= self.index_capacity:
            return
        capacity = _align_up(max(needed, self.index_capacity * 2), 4096)
        logger.debug(f"growing ImGui index buffer: {self.index_capacity} -> {capacity}")
        self.index_buffer = utils.create_buffer(
            self.device, "ImGui Index Buffer", capacity, wgpu.BufferUsage.INDEX
        )
        self.index_capacity = capacity

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
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
                write_mask=wgpu.ColorWriteMask.ALL,
            )
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

        self.bind_group_layout = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        )
        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[self.bind_group_layout])

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

        # Bind groups reference the old layout / uniform buffer, so they are
        # invalid once the pipeline is rebuilt.
        self.image_bind_groups.clear()
        logger.debug("create_pipeline done")

    # ------------------------------------------------------------------
    # Texture management (ImGui >= 1.92 backend-managed textures)
    # ------------------------------------------------------------------

    def update_textures(self, draw_data: imgui.DrawData) -> None:
        """Service every texture ImGui wants created, updated or destroyed.

        Must run before the render pass is opened: create_image_bind_group()
        needs a live texture view, and write_texture() targeting a texture that
        is already bound in an open pass is asking for trouble.
        """
        for tex in draw_data.textures:
            if tex.status != imgui.TextureStatus.OK:
                self.update_texture(tex)

    def update_texture(self, tex: imgui.TextureData) -> None:
        status = tex.status

        if status == imgui.TextureStatus.WANT_CREATE:
            self.create_texture(tex)
        elif status == imgui.TextureStatus.WANT_UPDATES:
            self.upload_texture(tex)
        elif status == imgui.TextureStatus.WANT_DESTROY:
            self.destroy_texture(tex)

    def create_texture(self, tex: imgui.TextureData) -> None:
        width = tex.width
        height = tex.height

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
        tex.set_tex_id(texture.id)

        logger.debug(f"ImGuiVu: created texture id={texture.id} size=({width}x{height})")

        self.upload_texture(tex, texture=texture)

    def upload_texture(self, tex: imgui.TextureData, texture: Texture2D | None = None) -> None:
        if texture is None:
            texture = ResourceManager().texture_kit.get(tex.tex_id)
            if texture is None:
                logger.warning(f"ImGuiVu: missing texture id={tex.tex_id}")
                tex.set_status(imgui.TextureStatus.DESTROYED)
                return

        width = tex.width
        height = tex.height
        bpp = tex.bytes_per_pixel

        # Full-surface upload. ImGui also exposes per-frame dirty rects; if font
        # atlas churn ever shows up in a profile, switch to those instead.
        self.queue.write_texture(
            wgpu.TexelCopyTextureInfo(
                texture=texture.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            tex.pixels,
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=width * bpp,
                rows_per_image=height,
            ),
            wgpu.Extent3D(width, height, 1),
        )

        tex.set_status(imgui.TextureStatus.OK)

    def destroy_texture(self, tex: imgui.TextureData) -> None:
        tex_id = tex.tex_id
        logger.debug(f"ImGuiVu: destroying texture id={tex_id}")

        # Drop the cached bind group first: it holds a view into the texture.
        self.image_bind_groups.pop(tex_id, None)

        texture = ResourceManager().texture_kit.get(tex_id)
        if texture is not None:
            texture.destroy()
            ResourceManager().texture_kit.remove(texture)

        tex.set_tex_id(TEXTURE_ID_INVALID)
        tex.set_status(imgui.TextureStatus.DESTROYED)

    def create_image_bind_group(self, tex_id: int) -> wgpu.BindGroup:
        texture = ResourceManager().texture_kit.get(tex_id)
        if texture is None:
            raise RuntimeError(f"ImGuiVu: no texture registered for id={tex_id}")

        bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, buffer=self.uniform_buffer, size=self.uniform_buffer_size),
            wgpu.BindGroupEntry(binding=1, sampler=self.sampler.sampler),
            wgpu.BindGroupEntry(binding=2, texture_view=texture.view),
        ]

        bind_group_desc = wgpu.BindGroupDescriptor(
            label=f"ImGui Texture Bind Group {tex_id}",
            layout=self.bind_group_layout,
            entries=bindgroup_entries,
        )

        return self.device.create_bind_group(bind_group_desc)

    def get_image_bind_group(self, tex_id: int) -> wgpu.BindGroup:
        bind_group = self.image_bind_groups.get(tex_id)
        if bind_group is None:
            bind_group = self.create_image_bind_group(tex_id)
            self.image_bind_groups[tex_id] = bind_group
        return bind_group

    # ------------------------------------------------------------------
    # Geometry upload
    # ------------------------------------------------------------------

    def upload_draw_data(self, draw_data: imgui.DrawData) -> list[tuple[int, int]]:
        """Pack every command list into the shared buffers with a single write each.

        Returns the (vertex_base, index_base) pair for each command list, in
        element units. Writing per-cmd-list would put us on non-4-aligned
        offsets whenever ImDrawIdx is 16-bit, which WebGPU rejects.
        """
        vtx_blob = bytearray()
        idx_blob = bytearray()
        offsets: list[tuple[int, int]] = []

        vtx_base = 0
        idx_base = 0

        for commands in draw_data.cmd_lists:
            offsets.append((vtx_base, idx_base))
            vtx_blob += commands.vtx_buffer_data
            idx_blob += commands.idx_buffer_data
            vtx_base += commands.vtx_buffer_size
            idx_base += commands.idx_buffer_size

        # writeBuffer size must be a 4-byte multiple; 16-bit indices can land odd.
        idx_blob += b"\x00" * (_align_up(len(idx_blob), COPY_ALIGNMENT) - len(idx_blob))

        self.grow_vertex_buffer(len(vtx_blob))
        self.grow_index_buffer(len(idx_blob))

        if vtx_blob:
            utils.write_buffer(self.device, self.vertex_buffer, 0, bytes(vtx_blob))
        if idx_blob:
            utils.write_buffer(self.device, self.index_buffer, 0, bytes(idx_blob))

        return offsets

    # ------------------------------------------------------------------
    # Draw recording
    # ------------------------------------------------------------------

    def record_draw_data(
        self,
        draw_data: imgui.DrawData,
        pass_enc: wgpu.RenderPassEncoder,
        offsets: list[tuple[int, int]],
        fb_size: glm.vec2,
    ) -> None:
        clip_pos   = glm.vec2(draw_data.display_pos[0], draw_data.display_pos[1])
        clip_scale = glm.vec2(draw_data.framebuffer_scale[0], draw_data.framebuffer_scale[1])

        for commands, (vtx_base, idx_base) in zip(draw_data.cmd_lists, offsets):
            for command in commands:
                if command.user_callback:
                    command.user_callback(commands, command)
                    continue

                cr = command.clip_rect
                clip_min = glm.vec2((cr[0] - clip_pos.x) * clip_scale.x,
                                    (cr[1] - clip_pos.y) * clip_scale.y)
                clip_max = glm.vec2((cr[2] - clip_pos.x) * clip_scale.x,
                                    (cr[3] - clip_pos.y) * clip_scale.y)

                clip_min = glm.max(clip_min, glm.vec2(0.0))
                clip_max = glm.min(clip_max, fb_size)
                if clip_max.x <= clip_min.x or clip_max.y <= clip_min.y:
                    continue

                pass_enc.set_bind_group(0, self.get_image_bind_group(command.texture_id))
                pass_enc.set_scissor_rect(
                    int(clip_min.x), int(clip_min.y),
                    int(clip_max.x - clip_min.x), int(clip_max.y - clip_min.y),
                )
                pass_enc.draw_indexed(
                    command.elem_count, 1,
                    command.idx_offset + idx_base,
                    command.vtx_offset + vtx_base,
                    0,
                )

    # ------------------------------------------------------------------
    # Frame entry point
    # ------------------------------------------------------------------

    def render(self):
        composition = Composition.get_current()
        imgui.render()
        draw_data = imgui.get_draw_data()

        display_pos  = glm.vec2(draw_data.display_pos[0], draw_data.display_pos[1])
        display_size = glm.vec2(draw_data.display_size[0], draw_data.display_size[1])
        fb_scale     = glm.vec2(draw_data.framebuffer_scale[0], draw_data.framebuffer_scale[1])
        fb_size      = display_size * fb_scale

        if fb_size.x <= 0 or fb_size.y <= 0:
            return

        # --- upload phase: everything that touches the queue, before the pass
        self.update_textures(draw_data)
        offsets = self.upload_draw_data(draw_data)
        if not offsets:
            return

        left   = display_pos.x
        right  = display_pos.x + display_size.x
        top    = display_pos.y
        bottom = display_pos.y + display_size.y
        mvp = glm.ortho(left, right, bottom, top, -1.0, 1.0)

        uniforms = Uniforms()
        uniforms.mvp.data = cast_matrix4(mvp)
        uniforms.gamma = 1.0
        self.queue.write_buffer(self.uniform_buffer, 0, uniforms)

        # --- record phase
        renderer = Renderer.get_current()
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.easel.color_texture_view,
                load_op=wgpu.LoadOp.LOAD,
                store_op=wgpu.StoreOp.STORE,
            )
        ]
        renderpass = wgpu.RenderPassDescriptor(
            label="ImGui Render Pass", color_attachments=color_attachments
        )

        with composition.gpu() as encoder:
            pass_enc = encoder.begin_render_pass(renderpass)
            pass_enc.set_pipeline(self.pipeline)
            pass_enc.set_vertex_buffer(0, self.vertex_buffer)
            pass_enc.set_index_buffer(self.index_buffer, self.index_format)
            self.record_draw_data(draw_data, pass_enc, offsets, fb_size)
            pass_enc.end()