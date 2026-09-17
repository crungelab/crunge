"""
Nine-patch rendering from a single sprite (a texel-space region of a texture).

The sprite is split into nine slices by normalized insets. Corners are drawn
at their natural size; edges and center fill along their stretchable axes,
each axis either tiling or stretching (see Fill):

    TL  T  TR        T, B   fill along x
    L   C  R         L, R   fill along y
    BL  B  BR        C      fills along both

Repeating is done in the fragment shader, not with a REPEAT sampler. Sampler
address modes wrap the whole texture, so they can't wrap a region inside an
atlas (or a slice inside a single image). The shader wraps within the slice
and keeps samples half a texel inside it, so neighbouring slices and atlas
entries never bleed in.

All nine slices are drawn with one instanced draw call.
"""

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import numpy as np
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from .three_patch_kit import (
    MAT4_SIZE,
    Rect,
    create_quad_pipeline,
    create_texture,
    load_rgba,
    rect_model,
    texture_bgl_entries,
)


type TexelRect = tuple[float, float, float, float]  # x, y (top-left, rows down), width, height


class Fill(Enum):
    """How the middle slices fill their length along one axis."""

    TILE = auto()  # repeat at natural size; needs uniform lines along that axis
    STRETCH = auto()  # draw once, scaled; keeps gradients and shading intact


@dataclass
class Insets:
    """Border sizes as fractions of the sprite's width (left/right) or height (top/bottom)."""

    left: float
    top: float
    right: float
    bottom: float


@dataclass
class SpriteRegion:
    """
    Stand-in for the engine's Sprite: a texture plus a texel-space rect.

    NinePatch only reads `.texture` and `.rect`, so an engine Sprite with
    those attributes can be passed directly.
    """

    texture: wgpu.Texture
    rect: TexelRect


def load_sprite(device: wgpu.Device, queue: wgpu.Queue, path: Path) -> SpriteRegion:
    """A sprite covering a whole image."""
    im = load_rgba(path)
    height, width = im.shape[:2]
    return SpriteRegion(create_texture(device, queue, im), (0, 0, width, height))


# ---------------------------------------------------------------------------
# Slicing and layout
# ---------------------------------------------------------------------------


def split_sprite(rect: TexelRect, insets: Insets) -> list[TexelRect]:
    """
    Split a texel-space rect into nine slices, row by row from the top-left.

    Borders are rounded to whole texels so no texel column or row is shared
    between two slices.
    """
    x, y, width, height = rect

    left = round(width * insets.left)
    right = round(width * insets.right)
    top = round(height * insets.top)
    bottom = round(height * insets.bottom)

    columns = [(x, left), (x + left, width - left - right), (x + width - right, right)]
    rows = [(y, top), (y + top, height - top - bottom), (y + height - bottom, bottom)]

    return [(cx, ry, cw, rh) for ry, rh in rows for cx, cw in columns]


def _spans(start: float, length: float, lead: float, trail: float):
    """Three (start, length) spans: fixed lead, stretchable middle, fixed trail."""
    caps = lead + trail
    if caps > length and caps > 0:
        squash = length / caps
        lead *= squash
        trail *= squash
    middle = max(length - lead - trail, 0.0)
    return [(start, lead), (start + lead, middle), (start + lead + middle, trail)]


def layout_nine_patch(
    x: float,
    y: float,
    width: float,
    height: float,
    borders: tuple[float, float, float, float],
) -> list[Rect]:
    """
    Split a y-up destination rect into nine rects, in the same top-left-first
    order as split_sprite. Borders are (left, top, right, bottom) in destination
    units; if they don't fit they are squashed and the middle collapses to zero.
    """
    left, top, right, bottom = borders

    columns = _spans(x, width, left, right)
    # y-up: spans run bottom to top, so reverse to get the top row first
    rows = _spans(y, height, bottom, top)[::-1]

    return [(cx, ry, cw, rh) for ry, rh in rows for cx, cw in columns]


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------


NINE_PATCH_SHADER = """
@group(0) @binding(0) var sprite_sampler : sampler;
@group(0) @binding(1) var sprite_texture : texture_2d<f32>;

struct Uniforms {
  view_projection : mat4x4<f32>,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

struct PatchInstance {
  model : mat4x4<f32>,
  region : vec4<f32>,  // texel-space x, y (top-left), width, height
  tiles : vec2<f32>,   // repeat count along x and y; 1 = drawn once
  _pad : vec2<f32>,
}
@group(0) @binding(3) var<storage, read> instances : array<PatchInstance>;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) tile_uv : vec2<f32>,  // 0..tiles, top-left origin
  @location(1) @interpolate(flat) region : vec4<f32>,
}

@vertex
fn vs_main(
  @builtin(vertex_index) idx : u32,
  @builtin(instance_index) inst : u32,
) -> VertexOutput {
  // Triangle strip corners: 0=(0,0) 1=(1,0) 2=(0,1) 3=(1,1)
  let corner = vec2<f32>(f32(idx & 1u), f32((idx >> 1u) & 1u));
  let item = instances[inst];

  let pos = uniforms.view_projection * item.model * vec4<f32>(corner, 0.0, 1.0);

  // Flip to a top-left origin to match texel space, then scale so each whole
  // unit is one repeat of the slice. Tiling starts at the top-left.
  let tile_uv = vec2<f32>(corner.x, 1.0 - corner.y) * item.tiles;

  return VertexOutput(pos, tile_uv, item.region);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let texture_size = vec2<f32>(textureDimensions(sprite_texture));
  let origin = in.region.xy;
  let size = in.region.zw;

  // Wrap within the slice, in texels
  let texel = origin + fract(in.tile_uv) * size;

  // Stay half a texel inside the slice so neighbours never bleed in
  let inside = clamp(texel, origin + 0.5, origin + size - 0.5);

  // Gradients come from the unwrapped coordinate, so the wrap seam doesn't
  // spike mip selection if the texture ever gets mipmaps
  let unwrapped = in.tile_uv * size / texture_size;

  return textureSampleGrad(
    sprite_texture,
    sprite_sampler,
    inside / texture_size,
    dpdx(unwrapped),
    dpdy(unwrapped),
  );
}
"""

# Per-instance layout: mat4 model (16) + vec4 region (4) + vec2 tiles (2) + pad (2).
# 96 bytes with 16-byte alignment.
INSTANCE_FLOATS = 24
PATCH_COUNT = 9


class NinePatch:
    def __init__(
        self,
        gfx,
        device: wgpu.Device,
        queue: wgpu.Queue,
        sprite: SpriteRegion,
        insets: Insets,
        scale: float = 1.0,
        fill_x: Fill = Fill.TILE,
        fill_y: Fill = Fill.TILE,
    ):
        """
        `scale` converts texels to destination units: it sets the border
        thickness and the size of one repeat. `fill_x` / `fill_y` choose tiling
        or stretching for the middle column and middle row.
        """
        self.queue = queue
        self.scale = scale
        self.fill_x = fill_x
        self.fill_y = fill_y

        # ASSUMPTION: sprite.rect unpacks as (x, y, width, height) in texels,
        # top-left origin. Adapt here if the engine's rect type differs.
        self.slices = split_sprite(tuple(sprite.rect), insets)

        top_left = self.slices[0]
        bottom_right = self.slices[8]
        self.borders = (
            top_left[2] * scale,  # left
            top_left[3] * scale,  # top
            bottom_right[2] * scale,  # right
            bottom_right[3] * scale,  # bottom
        )

        # Regions never change; models and tile counts are filled in by set_rect
        self.instance_data = np.zeros((PATCH_COUNT, INSTANCE_FLOATS), dtype=np.float32)
        self.instance_data[:, 16:20] = self.slices
        self.instance_data[:, 20:22] = 1.0

        self.uniform_buffer = utils.create_buffer(
            device,
            "Nine patch uniform",
            MAT4_SIZE,
            wgpu.BufferUsage.UNIFORM,
        )

        # ASSUMPTION: utils.create_buffer adds COPY_DST
        self.instance_buffer = utils.create_buffer(
            device,
            "Nine patch instances",
            self.instance_data.nbytes,
            wgpu.BufferUsage.STORAGE,
        )

        bgl_entries = texture_bgl_entries() + [
            wgpu.BindGroupLayoutEntry(
                binding=3,
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(
                    type=wgpu.BufferBindingType.READ_ONLY_STORAGE
                ),
            ),
        ]

        self.pipeline, bind_group_layout = create_quad_pipeline(
            gfx, device, NINE_PATCH_SHADER, bgl_entries, "Nine Patch Pipeline"
        )

        # Default sampler (clamp-to-edge): wrapping happens in the shader
        sampler = device.create_sampler()

        self.bind_group = device.create_bind_group(
            wgpu.BindGroupDescriptor(
                label="Nine patch bind group",
                layout=bind_group_layout,
                entries=[
                    wgpu.BindGroupEntry(binding=0, sampler=sampler),
                    wgpu.BindGroupEntry(
                        binding=1, texture_view=sprite.texture.create_view()
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
        rects = layout_nine_patch(x, y, width, height, self.borders)

        for i, (rect, region) in enumerate(zip(rects, self.slices)):
            row, column = divmod(i, 3)
            _, _, dest_w, dest_h = rect
            _, _, src_w, src_h = region

            # Middle column (T, C, B) fills along x; middle row (L, C, R) along y.
            # A tile count of 1 draws the slice once across the rect, i.e. stretches it.
            tile_x = 1.0
            if column == 1 and self.fill_x is Fill.TILE and src_w > 0:
                tile_x = dest_w / (src_w * self.scale)

            tile_y = 1.0
            if row == 1 and self.fill_y is Fill.TILE and src_h > 0:
                tile_y = dest_h / (src_h * self.scale)

            # PyGLM exports a Fortran-ordered buffer; F order gives column-major
            self.instance_data[i, :16] = np.asarray(
                rect_model(rect), dtype=np.float32
            ).reshape(-1, order="F")
            self.instance_data[i, 20:22] = (tile_x, tile_y)

        self.queue.write_buffer(self.uniform_buffer, 0, view_projection)
        self.queue.write_buffer(self.instance_buffer, 0, self.instance_data)

    def draw(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.draw(4, PATCH_COUNT)