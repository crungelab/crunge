struct Node {
    transform : mat4x4<f32>,
}

@group({{BindGroupIndex.NODE}}) @binding({{NodeBindIndex.NODE_UNIFORM}}) var<uniform> node : Node;
