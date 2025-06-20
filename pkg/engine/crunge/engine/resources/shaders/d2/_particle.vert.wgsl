struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group({{BindGroupIndex.MODEL}}) @binding(1)  var<storage, read> particles: array<Particle>;
