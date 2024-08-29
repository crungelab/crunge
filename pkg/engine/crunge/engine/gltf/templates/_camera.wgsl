struct Camera {
    modelMatrix : mat4x4<f32>,
    transformMatrix : mat4x4<f32>,
    //normalMatrix: mat3x3<f32>,
    normalMatrix: mat4x4<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;
