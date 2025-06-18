struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    //viewport : vec2<f32>,
    position: vec3<f32>,
}

@group({{BindGroupIndex.CAMERA}}) @binding({{CameraBindIndex.CAMERA_UNIFORM}}) var<uniform> camera : Camera;
