{% include '_camera.wgsl' %}
{% include '_model.wgsl' %}


struct Material {
    color : vec4<f32>,
}

//@group({{BindGroupIndex.MODEL}}) @binding({{MaterialBindIndex.MODEL_UNIFORM}}) var<uniform> material : Material;

struct VertexInput {
  @location(0) pos: vec4<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) color : vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = camera.projection * camera.view * model.transform * in.pos;
  return VertexOutput(vert_pos, model.color);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
    return in.color;
}
