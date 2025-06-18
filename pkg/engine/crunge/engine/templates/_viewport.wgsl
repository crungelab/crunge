struct Viewport {
    size : vec2<f32>,
    //_padding : vec2<f32>, // Padding to ensure 16-byte alignment
}

@group({{BindGroupIndex.VIEWPORT}}) @binding({{ViewportBindIndex.VIEWPORT_UNIFORM}}) var<uniform> viewport : Viewport;
