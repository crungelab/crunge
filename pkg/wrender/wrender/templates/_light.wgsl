struct LightUniform {
    position: vec3<f32>,
    color: vec3<f32>,
    range: f32,
    intensity: f32,
}
@group(0) @binding(1) var<uniform> lightUniform : LightUniform;

const LightKind_Point = 0u;

const LightKind_Spot = 1u;

const LightKind_Directional = 2u;

struct Light {
  kind : u32,
  v : vec3<f32>,
  color : vec3<f32>,
  range : f32,
  intensity : f32,
}
