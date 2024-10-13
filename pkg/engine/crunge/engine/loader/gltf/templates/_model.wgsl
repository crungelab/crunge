struct Model {
    modelMatrix : mat4x4<f32>,
    //normalMatrix: mat3x3<f32>,
    normalMatrix: mat4x4<f32>,
}
@group(3) @binding(0) var<uniform> model : Model;
