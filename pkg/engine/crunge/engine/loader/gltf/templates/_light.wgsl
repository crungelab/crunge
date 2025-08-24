struct AmbientLightUniform {
    color: vec3<f32>,
    _pad0: f32, // Padding to prevent the  WGSL compiler from sucking up a float after a vec3.
    energy: f32,
}
@group(1) @binding(0) var<uniform> ambientLightUniform : AmbientLightUniform;

struct AmbientLight {
  color : vec3<f32>,
  energy : f32,
}

struct LightUniform {
    position: vec3<f32>,
    color: vec3<f32>,
    _pad0: f32, // Padding to prevent the  WGSL compiler from sucking up a float after a vec3.
    energy: f32,
    range: f32,
}
@group(1) @binding(1) var<uniform> lightUniform : LightUniform;

const LightKind_Point = 0u;

const LightKind_Spot = 1u;

const LightKind_Directional = 2u;

struct Light {
  kind : u32,
  position: vec3<f32>,
  v : vec3<f32>,
  color : vec3<f32>,
  energy : f32,
  range : f32,
}
