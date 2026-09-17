"""
Three-patch rendering: a stretchable middle between two fixed-aspect caps.

Two renderers share the same layout rules and the same small API
(`set_rect` once per frame, `draw` inside a render pass):

- ThreePatch: one texture, uniform buffer and bind group per patch;
  three draw calls.
- InstancedThreePatch: the three images packed into one atlas, per-patch
  data in a storage buffer; one draw call.

Images are listed in reading order: left/middle/right for a row,
top/middle/bottom for a column. Rects are y-up with a bottom-left origin.
"""

from enum import Enum, auto
from pathlib import Path

from loguru import logger
import numpy as np
import imageio.v3 as iio
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils


type Rect = tuple[float, float, float, float]  # x, y, width, height
type Size = tuple[int, int]  # width, height

MAT4_SIZE = 4 * 16


class Orientation(Enum):
    ROW = auto()
    COLUMN = auto()


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------


def layout_three_patch(
    orientation: Orientation,
    sizes: list[Size],
    x: float,
    y: float,
    width: float,
    height: float,
) -> list[Rect]:
    """
    Split the rect into three patch rects, in the same order as the images.

    Caps keep their aspect ratio across the fixed dimension (height for a row,
    width for a column) and the middle takes the remaining length. If the caps
    alone are longer than the rect, they are squashed to fit and the middle
    collapses to zero.
    """
    (start_w, start_h), _, (end_w, end_h) = sizes

    if orientation is Orientation.ROW:
        length = width
        start = start_w * height / start_h
        end = end_w * height / end_h
    else:
        length = height
        start = start_h * width / start_w
        end = end_h * width / end_w

    caps = start + end
    if caps > length and caps > 0:
        squash = length / caps
        start *= squash
        end *= squash
    middle = max(length - start - end, 0.0)

    if orientation is Orientation.ROW:
        return [
            (x, y, start, height),
            (x + start, y, middle, height),
            (x + start + middle, y, end, height),
        ]

    # Column is y-up, so the first image (top cap) sits at the highest y
    return [
        (x, y + end + middle, width, start),
        (x, y + end, width, middle),
        (x, y, width, end),
    ]


def rect_model(rect: Rect) -> glm.mat4:
    """Model matrix mapping the 0..1 unit quad onto the rect."""
    x, y, width, height = rect
    model = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0))
    return glm.scale(model, glm.vec3(width, height, 1))


# ---------------------------------------------------------------------------
# Shared GPU helpers
# ---------------------------------------------------------------------------


def load_rgba(path: Path) -> np.ndarray:
    # Force RGBA so palette or RGB PNGs still match the texture format
    im = iio.imread(path, mode="RGBA")
    logger.debug(f"{path.name}: {im.shape}")
    return im


def create_texture(device: wgpu.Device, queue: wgpu.Queue, im: np.ndarray) -> wgpu.Texture:
    height, width, channels = im.shape

    descriptor = wgpu.TextureDescriptor(
        dimension=wgpu.TextureDimension.E2D,
        size=wgpu.Extent3D(width, height, 1),
        sample_count=1,
        format=wgpu.TextureFormat.RGBA8_UNORM,
        mip_level_count=1,
        usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
    )

    texture = device.create_texture(descriptor)

    queue.write_texture(
        wgpu.TexelCopyTextureInfo(
            texture=texture,
            mip_level=0,
            origin=wgpu.Origin3D(0, 0, 0),
            aspect=wgpu.TextureAspect.ALL,
        ),
        im,
        wgpu.TexelCopyBufferLayout(
            offset=0,
            bytes_per_row=channels * width,
            rows_per_image=height,
        ),
        wgpu.Extent3D(width, height, 1),
    )

    return texture


def texture_bgl_entries() -> list[wgpu.BindGroupLayoutEntry]:
    """Bindings 0-2 used by both renderers: sampler, texture, mat4 uniform."""
    return [
        wgpu.BindGroupLayoutEntry(
            binding=0,
            visibility=wgpu.ShaderStage.FRAGMENT,
            sampler=wgpu.SamplerBindingLayout(type=wgpu.SamplerBindingType.FILTERING),
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


def create_quad_pipeline(
    gfx,
    device: wgpu.Device,
    shader_code: str,
    bgl_entries: list[wgpu.BindGroupLayoutEntry],
    label: str,
) -> tuple[wgpu.RenderPipeline, wgpu.BindGroupLayout]:
    """Alpha-blended triangle-strip pipeline with no vertex buffers."""
    shader_module = gfx.create_shader_module(shader_code)

    # Straight (non-premultiplied) alpha blending for the PNG transparency
    # ASSUMPTION: BlendState / BlendComponent / BlendOperation / BlendFactor
    # binding names, and the `blend` field on ColorTargetState
    blend_state = wgpu.BlendState(
        color=wgpu.BlendComponent(
            operation=wgpu.BlendOperation.ADD,
            src_factor=wgpu.BlendFactor.SRC_ALPHA,
            dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
        ),
        alpha=wgpu.BlendComponent(
            operation=wgpu.BlendOperation.ADD,
            src_factor=wgpu.BlendFactor.ONE,
            dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
        ),
    )

    fragment_state = wgpu.FragmentState(
        module=shader_module,
        entry_point="fs_main",
        targets=[
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
            )
        ],
    )

    vertex_state = wgpu.VertexState(
        module=shader_module,
        entry_point="vs_main",
    )

    primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

    bind_group_layout = device.create_bind_group_layout(
        wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
    )

    pipeline_layout = device.create_pipeline_layout(
        wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bind_group_layout])
    )

    pipeline = device.create_render_pipeline(
        wgpu.RenderPipelineDescriptor(
            label=label,
            layout=pipeline_layout,
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragment_state,
        )
    )

    return pipeline, bind_group_layout


# ---------------------------------------------------------------------------
# Per-patch renderer: three textures, three draws
# ---------------------------------------------------------------------------


PER_PATCH_SHADER = """
@group(0) @binding(0) var patch_sampler : sampler;
@group(0) @binding(1) var patch_texture : texture_2d<f32>;

struct Uniforms {
  model_view_projection : mat4x4<f32>,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv : vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx : u32) -> VertexOutput {
  // Triangle strip corners: 0=(0,0) 1=(1,0) 2=(0,1) 3=(1,1)
  let corner = vec2<f32>(f32(idx & 1u), f32((idx >> 1u) & 1u));
  let pos = uniforms.model_view_projection * vec4<f32>(corner, 0.0, 1.0);

  // Flip v so image row 0 lands at the top
  let uv = vec2<f32>(corner.x, 1.0 - corner.y);

  return VertexOutput(pos, uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return textureSample(patch_texture, patch_sampler, in.uv);
}
"""


class ThreePatch:
    def __init__(
        self,
        gfx,
        device: wgpu.Device,
        queue: wgpu.Queue,
        image_paths: list[Path],
        orientation: Orientation,
    ):
        self.queue = queue
        self.orientation = orientation

        images = [load_rgba(path) for path in image_paths]
        self.sizes: list[Size] = [(im.shape[1], im.shape[0]) for im in images]

        self.pipeline, bind_group_layout = create_quad_pipeline(
            gfx, device, PER_PATCH_SHADER, texture_bgl_entries(), "Three Patch Pipeline"
        )

        sampler = device.create_sampler()

        self.textures: list[wgpu.Texture] = []
        self.uniform_buffers: list[wgpu.Buffer] = []
        self.bind_groups: list[wgpu.BindGroup] = []

        for i, im in enumerate(images):
            texture = create_texture(device, queue, im)

            uniform_buffer = utils.create_buffer(
                device,
                f"Three patch uniform {i}",
                MAT4_SIZE,
                wgpu.BufferUsage.UNIFORM,
            )

            bind_group = device.create_bind_group(
                wgpu.BindGroupDescriptor(
                    label=f"Three patch bind group {i}",
                    layout=bind_group_layout,
                    entries=[
                        wgpu.BindGroupEntry(binding=0, sampler=sampler),
                        wgpu.BindGroupEntry(binding=1, texture_view=texture.create_view()),
                        wgpu.BindGroupEntry(
                            binding=2, buffer=uniform_buffer, size=MAT4_SIZE
                        ),
                    ],
                )
            )

            self.textures.append(texture)
            self.uniform_buffers.append(uniform_buffer)
            self.bind_groups.append(bind_group)

    def set_rect(
        self, view_projection: glm.mat4, x: float, y: float, width: float, height: float
    ):
        rects = layout_three_patch(self.orientation, self.sizes, x, y, width, height)
        for buffer, rect in zip(self.uniform_buffers, rects):
            self.queue.write_buffer(buffer, 0, view_projection * rect_model(rect))

    def draw(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.pipeline)
        for bind_group in self.bind_groups:
            pass_enc.set_bind_group(0, bind_group)
            pass_enc.draw(4)


# ---------------------------------------------------------------------------
# Instanced renderer: one atlas, one draw
# ---------------------------------------------------------------------------


INSTANCED_SHADER = """
@group(0) @binding(0) var atlas_sampler : sampler;
@group(0) @binding(1) var atlas : texture_2d<f32>;

struct Uniforms {
  view_projection : mat4x4<f32>,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

struct PatchInstance {
  model : mat4x4<f32>,
  uv_rect : vec4<f32>,  // u0, v0 (top), u1, v1 (bottom) in atlas space
}
@group(0) @binding(3) var<storage, read> instances : array<PatchInstance>;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv : vec2<f32>,
}

@vertex
fn vs_main(
  @builtin(vertex_index) idx : u32,
  @builtin(instance_index) inst : u32,
) -> VertexOutput {
  // Triangle strip corners: 0=(0,0) 1=(1,0) 2=(0,1) 3=(1,1)
  // Each instance restarts the strip, so the same four indices work for every patch.
  let corner = vec2<f32>(f32(idx & 1u), f32((idx >> 1u) & 1u));
  let item = instances[inst];

  let pos = uniforms.view_projection * item.model * vec4<f32>(corner, 0.0, 1.0);

  // The top of the quad (corner.y = 1) maps to the top of the atlas region (v0)
  let uv = vec2<f32>(
    mix(item.uv_rect.x, item.uv_rect.z, corner.x),
    mix(item.uv_rect.w, item.uv_rect.y, corner.y),
  );

  return VertexOutput(pos, uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return textureSample(atlas, atlas_sampler, in.uv);
}
"""

ATLAS_PADDING = 1

# Per-instance layout: mat4 model (16 floats) + vec4 uv_rect (4 floats).
# 80 bytes with 16-byte alignment, so the WGSL struct needs no padding.
INSTANCE_FLOATS = 20


def build_atlas(
    images: list[np.ndarray], padding: int = ATLAS_PADDING
) -> tuple[np.ndarray, list[tuple[float, float, float, float]]]:
    """
    Pack images left to right into one RGBA array.

    Each image is surrounded by `padding` pixels copied from its own edge, so
    sampling right at a region's border can't pick up a neighbour's texels.
    Returns the atlas and each image's (u0, v0, u1, v1) rect, v0 being the top.
    """
    padded = [
        np.pad(im, ((padding, padding), (padding, padding), (0, 0)), mode="edge")
        for im in images
    ]

    atlas_width = sum(p.shape[1] for p in padded)
    atlas_height = max(p.shape[0] for p in padded)
    atlas = np.zeros((atlas_height, atlas_width, 4), dtype=np.uint8)

    uv_rects = []
    x = 0
    for im, p in zip(images, padded):
        padded_h, padded_w = p.shape[:2]
        atlas[0:padded_h, x : x + padded_w] = p

        im_h, im_w = im.shape[:2]
        uv_rects.append(
            (
                (x + padding) / atlas_width,
                padding / atlas_height,
                (x + padding + im_w) / atlas_width,
                (padding + im_h) / atlas_height,
            )
        )
        x += padded_w

    return atlas, uv_rects


class InstancedThreePatch:
    def __init__(
        self,
        gfx,
        device: wgpu.Device,
        queue: wgpu.Queue,
        image_paths: list[Path],
        orientation: Orientation,
    ):
        self.queue = queue
        self.orientation = orientation

        images = [load_rgba(path) for path in image_paths]
        self.sizes: list[Size] = [(im.shape[1], im.shape[0]) for im in images]

        atlas, uv_rects = build_atlas(images)
        logger.debug(f"atlas: {atlas.shape}")
        self.atlas_texture = create_texture(device, queue, atlas)

        # UV rects never change; model matrices are filled in by set_rect
        self.instance_data = np.zeros((len(images), INSTANCE_FLOATS), dtype=np.float32)
        self.instance_data[:, 16:20] = uv_rects

        self.uniform_buffer = utils.create_buffer(
            device,
            "Instanced three patch uniform",
            MAT4_SIZE,
            wgpu.BufferUsage.UNIFORM,
        )

        # ASSUMPTION: utils.create_buffer adds COPY_DST (as it must for the
        # uniform buffers, which are written with queue.write_buffer)
        self.instance_buffer = utils.create_buffer(
            device,
            "Instanced three patch instances",
            self.instance_data.nbytes,
            wgpu.BufferUsage.STORAGE,
        )

        bgl_entries = texture_bgl_entries() + [
            wgpu.BindGroupLayoutEntry(
                binding=3,
                visibility=wgpu.ShaderStage.VERTEX,
                # ASSUMPTION: READ_ONLY_STORAGE binding name
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]

        self.pipeline, bind_group_layout = create_quad_pipeline(
            gfx, device, INSTANCED_SHADER, bgl_entries, "Instanced Three Patch Pipeline"
        )

        sampler = device.create_sampler()

        self.bind_group = device.create_bind_group(
            wgpu.BindGroupDescriptor(
                label="Instanced three patch bind group",
                layout=bind_group_layout,
                entries=[
                    wgpu.BindGroupEntry(binding=0, sampler=sampler),
                    wgpu.BindGroupEntry(
                        binding=1, texture_view=self.atlas_texture.create_view()
                    ),
                    wgpu.BindGroupEntry(
                        binding=2, buffer=self.uniform_buffer, size=MAT4_SIZE
                    ),
                    wgpu.BindGroupEntry(
                        binding=3,
                        buffer=self.instance_buffer,
                        size=self.instance_data.nbytes,
                    ),
                ],
            )
        )

    def set_rect(
        self, view_projection: glm.mat4, x: float, y: float, width: float, height: float
    ):
        rects = layout_three_patch(self.orientation, self.sizes, x, y, width, height)
        for i, rect in enumerate(rects):
            # PyGLM exports matrices column by column, so flattening the numpy
            # view gives the column-major order WGSL expects
            self.instance_data[i, :16] = np.asarray(
                rect_model(rect), dtype=np.float32
            ).reshape(-1)

        self.queue.write_buffer(self.uniform_buffer, 0, view_projection)
        # ASSUMPTION: write_buffer accepts any buffer-protocol object, as it
        # does for glm matrices
        self.queue.write_buffer(self.instance_buffer, 0, self.instance_data)

    def draw(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        # ASSUMPTION: draw(vertex_count, instance_count) positional order
        pass_enc.draw(4, len(self.sizes))
