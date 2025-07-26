struct Viewport {
    size : vec2<f32>,
}

@group({{BindGroupIndex.SCENE}}) @binding({{SceneBindIndex.VIEWPORT_UNIFORM}}) var<uniform> viewport : Viewport;
@group({{BindGroupIndex.SCENE}}) @binding({{SceneBindIndex.SNAPSHOT_TEXTURE}}) var snapshotTexture : texture_2d<f32>;
@group({{BindGroupIndex.SCENE}}) @binding({{SceneBindIndex.SNAPSHOT_SAMPLER}}) var snapshotSampler: sampler;
