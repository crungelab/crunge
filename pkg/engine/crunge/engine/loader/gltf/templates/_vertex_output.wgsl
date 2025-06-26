struct VertexOutput {
    @builtin(position) position : vec4<f32>,
    {%- for attribute in vertex_output.attributes %}
    @location({{ attribute.location }}) {{ attribute.name }}: {{ attribute.type }},
    {%- endfor %}
}
