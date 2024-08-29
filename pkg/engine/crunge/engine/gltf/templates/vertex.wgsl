{% include '_vertex_input.wgsl' %}
{% include '_vertex_output.wgsl' %}
{% include '_camera.wgsl' %}

@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.frag_pos = (camera.modelMatrix * input.pos).xyz;
    output.vertex_pos = camera.transformMatrix * input.pos;
    //output.normal = camera.normalMatrix * input.normal;
    output.normal = normalize((camera.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz);

    {% include '_assignments.wgsl' %}
    return output;
}
