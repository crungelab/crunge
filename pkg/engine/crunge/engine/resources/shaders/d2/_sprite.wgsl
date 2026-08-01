const FLIP_H: u32 = 1u;
const FLIP_V: u32 = 2u;
const FLIP_D: u32 = 4u;

fn compute_uv(idx: u32, rect: vec4<f32>, tex_size: vec2<f32>, flip_flags: u32) -> vec2<f32> {
    // Normalized texture coordinates with half-pixel offsets
    let u0 = (rect.x + 0.5) / tex_size.x;
    let u1 = (rect.x + rect.z - 0.5) / tex_size.x;
    let v0 = (rect.y + 0.5) / tex_size.y;
    let v1 = (rect.y + rect.w - 0.5) / tex_size.y;

    // idx: 0 = bottom-left, 1 = bottom-right, 2 = top-left, 3 = top-right.
    // Geometry is Y-up and the texture is Y-down, hence v1 on the bottom row.
    var uvs = array<vec2<f32>, 4>(
        vec2<f32>(u0, v1), // BL
        vec2<f32>(u1, v1), // BR
        vec2<f32>(u0, v0), // TL
        vec2<f32>(u1, v0)  // TR
    );

    // Diagonal first: transpose across the TL-BR diagonal (swap BL and TR).
    if ((flip_flags & FLIP_D) != 0u) {
        uvs = array<vec2<f32>, 4>(uvs[3], uvs[1], uvs[2], uvs[0]);
    }

    // Then horizontal: swap left/right within each row.
    if ((flip_flags & FLIP_H) != 0u) {
        uvs = array<vec2<f32>, 4>(uvs[1], uvs[0], uvs[3], uvs[2]);
    }

    // Then vertical: swap top/bottom within each column.
    if ((flip_flags & FLIP_V) != 0u) {
        uvs = array<vec2<f32>, 4>(uvs[2], uvs[3], uvs[0], uvs[1]);
    }

    return uvs[idx];
}