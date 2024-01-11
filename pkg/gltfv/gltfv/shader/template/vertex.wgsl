struct VertexInput {
    @location(0) pos: vec4<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
    @location(3) tangent: vec4<f32>,
}
struct VertexOutput {
    @builtin(position) vertex_pos : vec4<f32>,
    @location(0) pos: vec4<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
    @location(3) tangent: vec3<f32>,
    @location(4) bitangent: vec3<f32>,
}

struct Camera {
    transformMatrix : mat4x4<f32>,
    normalMatrix: mat3x3<f32>,
    position: vec3<f32>,
}

@group(0) @binding(0) var<uniform> camera : Camera;

@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.vertex_pos = camera.transformMatrix * input.pos;
    output.normal = normalize(((camera.transformMatrix * vec4(input.normal.xyz, 0.0))).xyz);
    output.tangent = normalize(camera.normalMatrix * input.tangent.xyz);
    output.bitangent = (cross(output.normal, output.tangent) * input.tangent.w);
    output.uv = input.uv;
    return output;
}
