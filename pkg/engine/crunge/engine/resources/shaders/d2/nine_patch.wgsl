{% include '_camera.wgsl' %}
{% include '_material.wgsl' %}
{% include '_nine_patch_model.wgsl' %}
{% include '_node.wgsl' %}

{% include '_sprite.wgsl' %}
{% include '_nine_patch.wgsl' %}


struct VertexOutput {
    @builtin(position) vertex_pos : vec4<f32>,
    @location(0) @interpolate(flat) texture_layer: i32,
    @location(1) tile_uv: vec2<f32>, // 0..tiles, top-left origin
    @location(2) color: vec4<f32>,
    @location(3) @interpolate(flat) region: vec4<f32>, // cell x, y, width, height in flipped-sprite texels
    @location(4) @interpolate(flat) sprite_rect: vec4<f32>,
    @location(5) @interpolate(flat) texture_size: vec2<f32>,
    @location(6) @interpolate(flat) flip_flags: u32,
}

// Draw with draw(4, 9): one triangle-strip quad per cell.
@vertex
fn vs_main(
    @builtin(vertex_index) idx: u32,
    @builtin(instance_index) cell_index: u32,
) -> VertexOutput {
    // idx: 0 = bottom-left, 1 = bottom-right, 2 = top-left, 3 = top-right
    let corner = vec2<f32>(f32(idx & 1u), f32((idx >> 1u) & 1u));
    let node_size = max(node.size, vec2<f32>(1e-6));
    let cell = nine_patch_cell(cell_index, model, node_size);

    // Position within the node in local units, top-left origin
    let local_pos = vec2<f32>(
        mix(cell.dest.x, cell.dest.z, corner.x),
        mix(cell.dest.w, cell.dest.y, corner.y),
    );

    // node.transform scales the centered unit quad to the node's size, so
    // normalize by that size and recenter (y-up) before applying it
    let quad_pos = vec4<f32>(
        local_pos.x / node_size.x - 0.5,
        0.5 - local_pos.y / node_size.y,
        0.0,
        1.0,
    );
    let vert_pos = camera.projection * camera.view * node.transform * quad_pos;

    let tile_uv = vec2<f32>(corner.x, 1.0 - corner.y) * cell.tiles;
    let region = vec4<f32>(cell.source.xy, cell.source.zw - cell.source.xy);
    let color = model.color * node.color;

    return VertexOutput(
        vert_pos,
        model.texture_layer,
        tile_uv,
        color,
        region,
        model.spriteRect,
        model.textureSize,
        model.flipFlags,
    );
}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    let origin = in.region.xy;
    let extent = in.region.zw;
    let sprite_size = flip_size(in.sprite_rect.zw, in.flip_flags);

    // Wrap within the cell, staying half a texel inside it so neighbours never bleed in
    let wrapped = origin + fract(in.tile_uv) * extent;
    let inside = clamp(wrapped, origin + 0.5, origin + extent - 0.5);

    // Flipped-sprite texel -> source texel -> uv
    let source = in.sprite_rect.xy + flip_point(inside / sprite_size, in.flip_flags) * in.sprite_rect.zw;
    let uv = source / in.texture_size;

    // Gradients from the unwrapped coordinate, so the wrap seam doesn't affect mip selection
    let unwrapped = in.tile_uv * extent;
    let ddx = flip_vector(dpdx(unwrapped), in.flip_flags) / in.texture_size;
    let ddy = flip_vector(dpdy(unwrapped), in.flip_flags) / in.texture_size;

    let color = textureSampleGrad(myTexture, mySampler, uv, in.texture_layer, ddx, ddy);
    return color * in.color;
}
