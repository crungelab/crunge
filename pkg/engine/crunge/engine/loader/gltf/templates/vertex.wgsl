{% include '_vertex_input.wgsl' %}
{% include '_vertex_output.wgsl' %}
{% include '_camera.wgsl' %}
{% include '_model.wgsl' %}

@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.position = input.position;
    output.frag_pos = (model.modelMatrix * input.position).xyz;
    output.vertex_pos = camera.projection * camera.view * model.modelMatrix * input.position;
    //output.normal = normalize((model.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz);
    output.normal = (model.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz;

    {% include '_assignments.wgsl' %}
    return output;
}
