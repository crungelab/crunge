struct Model {
    transform : mat4x4<f32>,
}

@group({{BindGroupIndex.MODEL}}) @binding({{ModelBindIndex.MODEL_UNIFORM}}) var<storage, read> models: array<Model>;
