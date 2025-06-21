struct Viewport {
    size : vec2<f32>,
}

@group({{BindGroupIndex.CAMERA}}) @binding({{CameraBindIndex.VIEWPORT_UNIFORM}}) var<uniform> viewport : Viewport;
@group({{BindGroupIndex.CAMERA}}) @binding({{CameraBindIndex.SNAPSHOT_TEXTURE}}) var snapshotTexture : texture_2d<f32>;
@group({{BindGroupIndex.CAMERA}}) @binding({{CameraBindIndex.SNAPSHOT_SAMPLER}}) var snapshotSampler: sampler;
