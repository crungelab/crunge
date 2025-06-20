struct Particle {
    position: vec2<f32>,
    velocity: vec2<f32>,
    color: vec4<f32>,
    age: f32,
    lifespan: f32,
}
@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
