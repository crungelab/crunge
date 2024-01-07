struct Uniforms {
    transformMatrix : mat4x4<f32>,
    normalMatrix: mat3x3<f32>, // Added for correct normal transformations
}
@group(0) @binding(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
    @location(0) pos: vec4<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
    // Add tangent and bitangent if using normal maps
}
struct VertexOutput {
    @builtin(position) vertex_pos : vec4<f32>,
    @location(1) normal: vec3<f32>,
    @location(2) uv: vec2<f32>,
    // Pass tangent and bitangent to fragment shader if using normal maps
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
    var out: VertexOutput;
    out.vertex_pos = uniforms.transformMatrix * in.pos;
    out.normal = normalize(uniforms.normalMatrix * in.normal); // Transform the normal
    out.uv = in.uv;
    // Compute and pass tangent and bitangent if using normal maps
    return out;
}
