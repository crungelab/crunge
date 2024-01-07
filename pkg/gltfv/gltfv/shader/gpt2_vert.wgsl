struct Uniforms {
    transformMatrix: mat4x4<f32>,
    normalMatrix: mat3x3<f32>,
};

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

struct VertexInput {
    @location(0) pos: vec4<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
};

struct VertexOutput {
    @builtin(position) vertex_pos: vec4<f32>,
    @location(0) world_normal: vec3<f32>,
    @location(1) uv: vec2<f32>,
};

@vertex
fn vs_main(in: VertexInput) -> VertexOutput {
    var out: VertexOutput;
    out.vertex_pos = uniforms.transformMatrix * in.pos;
    out.world_normal = normalize(uniforms.normalMatrix * in.normal);
    out.uv = in.uv;
    return out;
}
