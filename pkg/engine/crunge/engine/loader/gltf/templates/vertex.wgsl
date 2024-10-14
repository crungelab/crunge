{% include '_vertex_input.wgsl' %}
{% include '_vertex_output.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_model.wgsl' %}

@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.frag_pos = (model.modelMatrix * input.pos).xyz;
    output.vertex_pos = camera.projection * camera.view * model.modelMatrix * input.pos;
    //output.normal = camera.normalMatrix * input.normal;
    output.normal = normalize((model.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz);

    {% include '_assignments.wgsl' %}
    return output;
}
