from ctypes import c_float, sizeof

from loguru import logger
import numpy as np

from freetype import Face

import PIL.Image

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Renderer

from ..demo import Demo


vs_shader_code = """
struct VertexOutput {
    @builtin(position) position: vec4<f32>,
    @location(0) uv: vec2<f32>,
};

@vertex
fn main(@location(0) pos: vec2<f32>,
        @location(1) uv: vec2<f32>) -> VertexOutput {
    var out: VertexOutput;
    out.position = vec4<f32>(pos, 0.0, 1.0);
    out.uv = vec2<f32>(uv.x, 1.0 - uv.y);  // flip vertically
    return out;
}
"""

fs_shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture: texture_2d<f32>;

@fragment
fn main(@location(0) uv: vec2<f32>) -> @location(0) vec4<f32> {
    let color = textureSample(myTexture, mySampler, uv);
    return vec4<f32>(color.rgb, color.a);
}
"""


index_data = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

vertex_data = np.array(
    [
        -0.5,
        0.5,
        0.0,
        1.0,  # top-left
        -0.5,
        -0.5,
        0.0,
        0.0,  # bottom-left
        0.5,
        -0.5,
        1.0,
        0.0,  # bottom-right
        0.5,
        0.5,
        1.0,
        1.0,  # top-right
    ],
    dtype=np.float32,
)


class FontAtlasDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    kWidth = 800
    kHeight = 600

    def __init__(self):
        super().__init__()

    def create_device_objects(self):
        self.create_buffers()
        self.create_textures()
        self.create_pipeline()

    def create_pipeline(self):
        vs_module = self.gfx.create_shader_module(vs_shader_code)
        fs_module = self.gfx.create_shader_module(fs_shader_code)

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

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=4 * sizeof(c_float),
                attributes=vertAttributes,
            )
        ]

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
            )
        ]

        fragmentState = wgpu.FragmentState(
            module=fs_module,
            entry_point="main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="main",
            buffers=vb_layouts,
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
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bgl])

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        view: wgpu.TextureView = self.texture.create_view()

        bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, texture_view=view),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entries=bindgroup_entries,
        )

        self.bindGroup = self.device.create_bind_group(bindGroupDesc)
        logger.debug(self.bindGroup)

        # exit()

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", index_data, wgpu.BufferUsage.INDEX
        )

    def create_textures(self):
        path = self.wnd.resource_root / "fonts" / "DroidSans.ttf"
        logger.debug(f"Loading font from {path}")
        if not path.exists():
            raise FileNotFoundError(f"Font file not found: {path}")

        face = Face(path.as_posix())
        face.set_pixel_sizes(0, 48)

        # Create a blank image (RGBA)
        atlas_size = (1024, 1024)
        atlas_image = PIL.Image.new("L", atlas_size, color=0)

        # Simple ASCII range
        start_char = 32
        end_char = 127

        pen_x, pen_y = 0, 0
        row_height = 0

        for char_code in range(start_char, end_char):
            face.load_char(chr(char_code))
            bitmap = face.glyph.bitmap
            w, h = bitmap.width, bitmap.rows

            if pen_x + w >= atlas_size[0]:
                pen_x = 0
                pen_y += row_height
                row_height = 0

            if pen_y + h >= atlas_size[1]:
                raise RuntimeError("Font atlas too small")

            glyph_image = PIL.Image.frombytes("L", (w, h), bytes(bitmap.buffer))
            atlas_image.paste(glyph_image, (pen_x, pen_y))

            pen_x += w + 1
            row_height = max(row_height, h)

        rgba_image = atlas_image.convert("RGBA")  # RGBA8_UNORM
        rgba_data = np.array(rgba_image, dtype=np.uint8)

        self.texture = self.device.create_texture(
            wgpu.TextureDescriptor(
                size=wgpu.Extent3D(*atlas_size, 1),
                mip_level_count=1,
                sample_count=1,
                dimension=wgpu.TextureDimension.E2D,
                format=wgpu.TextureFormat.RGBA8_UNORM,
                usage=wgpu.TextureUsage.TEXTURE_BINDING | wgpu.TextureUsage.COPY_DST,
            )
        )

        self.sampler = self.device.create_sampler()

        self.queue.write_texture(
            wgpu.TexelCopyTextureInfo(
                texture=self.texture, mip_level=0, origin=wgpu.Origin3D(0, 0, 0)
            ),
            rgba_data,
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=rgba_data.shape[1] * 4,
                rows_per_image=rgba_data.shape[0],
            ),
            wgpu.Extent3D(rgba_data.shape[1], rgba_data.shape[0], 1),
        )

    def draw(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                # view=renderer.texture_view,
                view=renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(6)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super().draw(renderer)


def main():
    FontAtlasDemo().run()


if __name__ == "__main__":
    main()
