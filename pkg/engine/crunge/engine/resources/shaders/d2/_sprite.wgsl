// Function to compute UV coordinates with optional flipping
fn compute_uv(idx: u32, rect: vec4<f32>, tex_size: vec2<f32>, flip_h: bool, flip_v: bool) -> vec2<f32> {
    // Normalized texture coordinates with half-pixel offsets
    let u0 = (rect.x + 0.5) / tex_size.x;
    let u1 = (rect.x + rect.z - 0.5) / tex_size.x;
    let v0 = (rect.y + 0.5) / tex_size.y;
    let v1 = (rect.y + rect.w - 0.5) / tex_size.y;

    // Flip the V coordinates
    let v0_flipped = v1;
    let v1_flipped = v0;

    // Reorder UVs for triangle strip
    var uvs = array<vec2<f32>, 4>(
        vec2<f32>(u0, v0_flipped), // Bottom-left
        vec2<f32>(u1, v0_flipped), // Bottom-right
        vec2<f32>(u0, v1_flipped), // Top-left
        vec2<f32>(u1, v1_flipped)  // Top-right
    );

    // Flip horizontally
    if (flip_v) {
        uvs = array<vec2<f32>, 4>(
            uvs[3], // Top-left -> Top-right
            uvs[2], // Bottom-left -> Bottom-right
            uvs[1], // Bottom-right -> Bottom-left
            uvs[0]  // Top-right -> Top-left
        );
    }

    // Flip vertically
    if (flip_h) {
        uvs = array<vec2<f32>, 4>(
            uvs[1], // Top-left -> Bottom-left
            uvs[0], // Bottom-left -> Top-left
            uvs[3], // Bottom-right -> Top-right
            uvs[2]  // Top-right -> Bottom-right
        );
    }

    return uvs[idx];
}
