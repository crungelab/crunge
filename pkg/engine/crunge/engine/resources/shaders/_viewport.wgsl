struct Viewport {
    size : vec2<f32>,
    //_padding : vec2<f32>, // Padding to ensure 16-byte alignment
}

@group({{GlobalBindGroupIndex.VIEWPORT}}) @binding({{ViewportBindIndex.VIEWPORT_UNIFORM}}) var<uniform> viewport : Viewport;
@group({{GlobalBindGroupIndex.VIEWPORT}}) @binding({{ViewportBindIndex.SAMPLER}}) var snapshotSampler: sampler;
@group({{GlobalBindGroupIndex.VIEWPORT}}) @binding({{ViewportBindIndex.TEXTURE}}) var snapshotTexture : texture_2d<f32>;
