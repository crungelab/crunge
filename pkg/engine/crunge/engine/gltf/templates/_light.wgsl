struct AmbientLightUniform {
    color: vec3<f32>,
    energy: f32,
}
@group(0) @binding(1) var<uniform> ambientLightUniform : AmbientLightUniform;

struct AmbientLight {
  color : vec3<f32>,
  energy : f32,
}

struct LightUniform {
    position: vec3<f32>,
    color: vec3<f32>,
    range: f32,
    energy: f32,
}
@group(0) @binding(2) var<uniform> lightUniform : LightUniform;

const LightKind_Point = 0u;

const LightKind_Spot = 1u;

const LightKind_Directional = 2u;

struct Light {
  kind : u32,
  position: vec3<f32>,
  v : vec3<f32>,
  color : vec3<f32>,
  range : f32,
  energy : f32,
}
