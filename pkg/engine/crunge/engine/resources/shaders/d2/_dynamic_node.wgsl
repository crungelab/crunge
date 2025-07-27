struct Node {
    transform : mat4x4<f32>,
    model_index : u32, // Index of the model in the models array
}

@group({{BindGroupIndex.NODE}}) @binding({{NodeBindIndex.NODE_UNIFORM}}) var<storage, read> nodes: array<Node>;
