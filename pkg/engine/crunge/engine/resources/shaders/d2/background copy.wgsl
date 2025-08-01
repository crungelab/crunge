{% include '_viewport.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_material.wgsl' %}
{% include '_model.wgsl' %}
{% include '_sprite.wgsl' %}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> VertexOutput {
    let x = f32((idx & 1u) << 1) - 1.0; // Generates -1.0 or 1.0
    let y = f32((idx & 2u) >> 1) * 2.0 - 1.0; // Generates -1.0 or 1.0

    let quad_pos = vec4<f32>(x, y, 0.0, 1.0);
    let vert_pos = camera.view * quad_pos;
    let rect = vec4<f32>(0, 0, viewport.size.x, viewport.size.y);

    let uv = compute_uv(
        idx,
        rect,
        material.textureSize,
        material.flipH != 0u,
        material.flipV != 0u
    );

    return VertexOutput(vert_pos, uv);
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let color = textureSample(myTexture, mySampler, in.uv);
    return color * material.color;
}
