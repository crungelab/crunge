// Requires FLIP_* from _sprite.wgsl and NinePatchModel from _nine_patch_model.wgsl.
//
// Layout happens against the sprite as it appears after flipping (the
// "flipped sprite"), so a flipped nine-patch is the nine-patch of the flipped
// image: borders and tiling follow the image, not the node.

const FILL_TILE_X: u32 = 1u;
const FILL_TILE_Y: u32 = 2u;

// Insets of the flipped sprite, as left, top, right, bottom.
fn flip_insets(insets: vec4<f32>, flags: u32) -> vec4<f32> {
    var e = insets;
    if ((flags & FLIP_D) != 0u) { e = e.yxwz; }
    if ((flags & FLIP_H) != 0u) { e = e.zyxw; }
    if ((flags & FLIP_V) != 0u) { e = e.xwzy; }
    return e;
}

// Size of the flipped sprite in texels.
fn flip_size(size: vec2<f32>, flags: u32) -> vec2<f32> {
    return select(size, size.yx, (flags & FLIP_D) != 0u);
}

// Normalized point in the flipped sprite -> normalized point in the source
// rect, both top-left origin. The same mapping compute_uv applies to corners.
fn flip_point(p: vec2<f32>, flags: u32) -> vec2<f32> {
    var q = p;
    if ((flags & FLIP_V) != 0u) { q.y = 1.0 - q.y; }
    if ((flags & FLIP_H) != 0u) { q.x = 1.0 - q.x; }
    if ((flags & FLIP_D) != 0u) { q = q.yx; }
    return q;
}

// Linear part of flip_point in texel units, for gradients.
fn flip_vector(v: vec2<f32>, flags: u32) -> vec2<f32> {
    var w = v;
    if ((flags & FLIP_V) != 0u) { w.y = -w.y; }
    if ((flags & FLIP_H) != 0u) { w.x = -w.x; }
    if ((flags & FLIP_D) != 0u) { w = w.yx; }
    return w;
}

struct NinePatchCell {
    dest : vec4<f32>, // x0, y0, x1, y1 in local units, top-left origin
    source : vec4<f32>, // x0, y0, x1, y1 in flipped-sprite texels, top-left origin
    tiles : vec2<f32>, // repeat counts; 1 = stretched across the cell
}

// Edges along one axis: [0, lead, length - trail, length].
// Borders that don't fit are squashed and the middle collapses to zero.
fn nine_patch_edges(length: f32, lead: f32, trail: f32) -> vec4<f32> {
    let caps = lead + trail;
    let k = select(1.0, length / max(caps, 1e-6), caps > length);
    return vec4<f32>(0.0, lead * k, length - trail * k, length);
}

// Cell 0..8, row by row from the top-left. `size` is the node's size in
// local units, the same size node.transform scales the unit quad to.
fn nine_patch_cell(index: u32, m: NinePatchModel, size: vec2<f32>) -> NinePatchCell {
    let sprite_size = flip_size(m.spriteRect.zw, m.flipFlags);
    let insets = flip_insets(m.insets, m.flipFlags);

    // Whole texels, so no texel row or column is shared between cells
    let lead = round(sprite_size * insets.xy); // left, top
    let trail = round(sprite_size * insets.zw); // right, bottom

    let src_x = vec4<f32>(0.0, lead.x, sprite_size.x - trail.x, sprite_size.x);
    let src_y = vec4<f32>(0.0, lead.y, sprite_size.y - trail.y, sprite_size.y);

    let dst_x = nine_patch_edges(size.x, lead.x * m.borderScale, trail.x * m.borderScale);
    let dst_y = nine_patch_edges(size.y, lead.y * m.borderScale, trail.y * m.borderScale);

    let col = index % 3u;
    let row = index / 3u;

    let dest = vec4<f32>(dst_x[col], dst_y[row], dst_x[col + 1u], dst_y[row + 1u]);
    let source = vec4<f32>(src_x[col], src_y[row], src_x[col + 1u], src_y[row + 1u]);

    let dest_size = dest.zw - dest.xy;
    let repeat_size = (source.zw - source.xy) * m.borderScale;

    // Middle column (T, C, B) fills along x; middle row (L, C, R) along y
    var tiles = vec2<f32>(1.0);
    if (col == 1u && (m.fillFlags & FILL_TILE_X) != 0u && repeat_size.x > 0.0) {
        tiles.x = dest_size.x / repeat_size.x;
    }
    if (row == 1u && (m.fillFlags & FILL_TILE_Y) != 0u && repeat_size.y > 0.0) {
        tiles.y = dest_size.y / repeat_size.y;
    }

    return NinePatchCell(dest, source, tiles);
}
