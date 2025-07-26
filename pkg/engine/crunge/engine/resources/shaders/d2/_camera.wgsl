struct Camera {
    projection : mat4x4<f32>,
    view : mat4x4<f32>,
    position: vec3<f32>,
}

@group({{BindGroupIndex.SCENE}}) @binding({{SceneBindIndex.CAMERA_UNIFORM}}) var<uniform> camera : Camera;
