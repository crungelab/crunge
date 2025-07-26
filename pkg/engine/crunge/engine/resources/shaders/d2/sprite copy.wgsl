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

    let quad_pos = vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0); // Scale quad by 0.5
    let vert_pos = camera.projection * camera.view * node.transform * quad_pos;

    // Calculate UV coordinates dynamically
    let rect = material.spriteRect;
    let tex_size = material.textureSize;

    // Compute UV for the current vertex with flipping
    let uv = compute_uv(
        idx,
        material.spriteRect,
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