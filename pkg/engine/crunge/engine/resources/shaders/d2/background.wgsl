{% include '_viewport.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_material.wgsl' %}
{% include '_model.wgsl' %}
{% include '_node.wgsl' %}

{% include '_sprite.wgsl' %}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) @interpolate(flat) texture_layer: i32,
  @location(1) uv: vec2<f32>,
  @location(2) color: vec4<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> VertexOutput {
    // Fullscreen quad in clip space corners
    let x = f32((idx & 1u) << 1) - 1.0;        // -1 or +1
    let y = f32((idx & 2u) >> 1) * 2.0 - 1.0;  // -1 or +1

    // IMPORTANT: For a true fullscreen background, don't apply camera transforms.
    // If you must keep your SpriteVu plumbing, use an identity view/proj for this draw.
    let quad_pos = vec4<f32>(x, y, 0.0, 1.0);
    let vert_pos = quad_pos;

    // Base UV in [0..1]
    let u0 = (x * 0.5) + 0.5;
    let v0 = (y * 0.5) + 0.5;

    // If your textures are appearing upside down, flip V here:
    // let v_base = 1.0 - v0;
    let v_base = 1.0 - v0;

    // --- COVER mapping ---
    // We want the texture to cover the viewport. That means we crop in UV space.
    let vp_aspect  = viewport.size.x / viewport.size.y;
    let tex_aspect = model.textureSize.x / model.textureSize.y;

    // uv_scale < 1 means "use a smaller region of the texture" (cropping).
    // uv_offset centers that crop.
    var uv_scale  = vec2<f32>(1.0, 1.0);
    var uv_offset = vec2<f32>(0.0, 0.0);

    if (tex_aspect > vp_aspect) {
        // Texture is wider than viewport: crop left/right => shrink U range
        let s = vp_aspect / tex_aspect;        // < 1
        uv_scale  = vec2<f32>(s, 1.0);
        uv_offset = vec2<f32>((1.0 - s) * 0.5, 0.0);
    } else {
        // Texture is taller than viewport: crop top/bottom => shrink V range
        let s = tex_aspect / vp_aspect;        // < 1
        uv_scale  = vec2<f32>(1.0, s);
        uv_offset = vec2<f32>(0.0, (1.0 - s) * 0.5);
    }

    let uv = vec2<f32>(u0, v_base) * uv_scale + uv_offset;

    return VertexOutput(vert_pos, model.texture_layer, uv, model.color);
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let color = textureSample(myTexture, mySampler, in.uv, in.texture_layer);
    return color * in.color;
}
