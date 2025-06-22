from dataclasses import dataclass

from loguru import logger

import numpy as np
from freetype import Face
import PIL.Image
import uharfbuzz as hb
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Renderer
from ..demo import Demo


from ctypes import (
    Structure,
    c_uint32,
    sizeof,
)

from crunge.engine.uniforms import Vec2


class GlyphUniform(Structure):
    _fields_ = [
        ("uv", Vec2),
        ("size", Vec2),
    ]


assert sizeof(GlyphUniform) % 16 == 0


class GlyphInstance(Structure):
    _fields_ = [
        ("position", Vec2),
        ("scale", Vec2),
        ("glyph_index", c_uint32),
        ("_pad1", c_uint32),
    ]


@dataclass
class GlyphData:
    uv: tuple
    size: tuple
    offset: tuple
    advance: tuple


vs_shader_code = """
struct GlyphInstance {
    position: vec2<f32>,
    scale: vec2<f32>,
    glyph_index: u32,
};

struct GlyphUV {
    uv: vec2<f32>,
    size: vec2<f32>,
};

@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture: texture_2d<f32>;
@group(0) @binding(2) var<storage, read> glyph_uvs: array<GlyphUV>;
@group(0) @binding(3) var<storage, read> glyph_instances: array<GlyphInstance>;

struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) uv: vec2<f32>,
};

@vertex
fn vs_main(@builtin(vertex_index) vertex_index: u32,
           @builtin(instance_index) instance_index: u32) -> VertexOutput {
    let instance = glyph_instances[instance_index];
    let uv_info = glyph_uvs[instance.glyph_index];

    // Get corner in [0,1] space
    let x = f32(vertex_index & 1u);
    let y = f32((vertex_index >> 1) & 1u);
    let corner = vec2<f32>(x, y);

    var out: VertexOutput;
    out.position = vec4<f32>(instance.position + corner * instance.scale, 0.0, 1.0);
    out.uv = uv_info.uv + corner * uv_info.size;
    return out;
}
"""

fs_shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture: texture_2d<f32>;

@fragment
fn main(@location(0) uv: vec2<f32>) -> @location(0) vec4<f32> {
    return textureSample(myTexture, mySampler, uv);
    //return vec4<f32>(1.0, 1.0, 1.0, 1.0);  // full white
}
"""


class InstancedTextDemo(Demo):
    def __init__(self):
        super().__init__()
        self.text = "Hello, WebGPU!"
        self.glyph_map: dict[int, GlyphData] = {}  # Maps character code to GlyphData

    def create_device_objects(self):
        self.create_textures()
        self.create_buffers()
        self.create_pipeline()

    def create_textures(self):
        path = self.wnd.resource_root / "fonts" / "DroidSans.ttf"
        face = Face(path.as_posix())
        face.set_pixel_sizes(0, 48)

        atlas_size = (1024, 1024)
        atlas_image = PIL.Image.new("L", atlas_size, color=0)

        pen_x, pen_y, row_height = 0, 0, 0

        for char_code in range(32, 127):
            face.load_char(char_code)
            bitmap = face.glyph.bitmap
            w, h = bitmap.width, bitmap.rows
            if pen_x + w >= atlas_size[0]:
                pen_x = 0
                pen_y += row_height
                row_height = 0

            glyph_index = face.get_char_index(char_code)

            self.glyph_map[glyph_index] = GlyphData(
                uv=(
                    pen_x / atlas_size[0],
                    pen_y / atlas_size[1],
                    w / atlas_size[0],
                    h / atlas_size[1],
                ),
                size=(w, h),
                offset=(face.glyph.bitmap_left, face.glyph.bitmap_top),
                advance=(face.glyph.advance.x / 64.0, face.glyph.advance.y / 64.0),
            )

            glyph_image = PIL.Image.frombytes("L", (w, h), bytes(bitmap.buffer))
            atlas_image.paste(glyph_image, (pen_x, pen_y))
            pen_x += w + 1
            row_height = max(row_height, h)

        rgba_image = atlas_image.convert("RGBA")
        rgba_data = np.array(rgba_image, dtype=np.uint8)

        self.texture = self.device.create_texture(
            wgpu.TextureDescriptor(
                size=wgpu.Extent3D(*atlas_size, 1),
                format=wgpu.TextureFormat.RGBA8_UNORM,
                usage=wgpu.TextureUsage.TEXTURE_BINDING | wgpu.TextureUsage.COPY_DST,
            )
        )
        self.sampler = self.device.create_sampler()

        self.queue.write_texture(
            wgpu.TexelCopyTextureInfo(texture=self.texture),
            rgba_data,
            wgpu.TexelCopyBufferLayout(bytes_per_row=rgba_data.shape[1] * 4),
            wgpu.Extent3D(rgba_data.shape[1], rgba_data.shape[0], 1),
        )

    def create_buffers(self):
        infos, positions = self.shape_text(self.text)

        instances = []
        uvs = [GlyphUniform() for _ in range(256)]
        cursor_x, cursor_y = -0.8, 0.5  # Top-left starting pos

        for info, pos in zip(infos, positions):
            gid = info.codepoint
            glyph_data = self.glyph_map.get(gid)
            if not glyph_data:
                continue  # Skip missing

            uv_x, uv_y, uv_w, uv_h = glyph_data.uv
            size_x, size_y = glyph_data.size
            offset_x, offset_y = glyph_data.offset
            logger.debug(f"Offset: {offset_x}, {offset_y}")
            advance_x, advance_y = glyph_data.advance

            glyph_index = gid  # Adjust for ASCII range
            logger.debug(f"Info: {info}, Position: {pos}, Glyph ID: {gid}")
            logger.debug(
                f"Glyph index: {glyph_index}, UV: {uv_x}, {uv_y}, Size: {size_x}, {size_y}"
            )
            uvs[glyph_index] = GlyphUniform(
                uv=Vec2(uv_x, uv_y),
                size=Vec2(uv_w, uv_h),
            )

            px = cursor_x + offset_x / self.width
            py = cursor_y + offset_y / self.height

            sx = size_x / self.width
            sy = -size_y / self.height

            instances.append(
                GlyphInstance(
                    position=Vec2(px, py),
                    scale=Vec2(sx, sy),
                    glyph_index=glyph_index,
                )
            )

            cursor_x += advance_x / self.width
            cursor_y += advance_y / self.height

        # logger.debug(f"Uvs: {uvs}")
        self.instance_count = len(instances)

        self.instance_buffer = utils.create_buffer_from_ctypes_array(
            self.device,
            "INSTANCE",
            (GlyphInstance * len(instances))(*instances),
            wgpu.BufferUsage.STORAGE,
        )

        self.uv_buffer = utils.create_buffer_from_ctypes_array(
            self.device,
            "UVS",
            (GlyphUniform * len(uvs))(*uvs),
            wgpu.BufferUsage.STORAGE,
        )

    def shape_text(self, text: str):
        path = self.wnd.resource_root / "fonts" / "DroidSans.ttf"
        with open(path, "rb") as f:
            font_data = f.read()
        hb_font = hb.Font(hb.Face(hb.Blob(font_data)))
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)
        return buf.glyph_infos, buf.glyph_positions

    def create_pipeline(self):
        vs_module = self.gfx.create_shader_module(vs_shader_code)
        fs_module = self.gfx.create_shader_module(fs_shader_code)

        color_target = wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
        vertex_state = wgpu.VertexState(module=vs_module, entry_point="vs_main")
        fragment_state = wgpu.FragmentState(
            module=fs_module, entry_point="main", targets=[color_target]
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
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=3,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bgl])

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragment_state,
            primitive=wgpu.PrimitiveState(
                topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP
            ),
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, texture_view=self.texture.create_view()),
            wgpu.BindGroupEntry(binding=2, buffer=self.uv_buffer),
            wgpu.BindGroupEntry(binding=3, buffer=self.instance_buffer),
        ]

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entries=bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(bind_group_desc)

    def draw(self, renderer: Renderer):
        encoder = self.device.create_command_encoder()
        render_pass = encoder.begin_render_pass(
            wgpu.RenderPassDescriptor(
                color_attachments=[
                    wgpu.RenderPassColorAttachment(
                        view=renderer.viewport.color_texture_view,
                        load_op=wgpu.LoadOp.CLEAR,
                        store_op=wgpu.StoreOp.STORE,
                        clear_value=wgpu.Color(0.0, 0.0, 0.0, 1.0),
                    )
                ],
            )
        )
        render_pass.set_pipeline(self.pipeline)
        render_pass.set_bind_group(0, self.bind_group)
        render_pass.draw(4, self.instance_count)
        render_pass.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])


def main():
    InstancedTextDemo().run()


if __name__ == "__main__":
    main()
