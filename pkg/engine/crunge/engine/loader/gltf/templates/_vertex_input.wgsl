struct VertexInput {
    {%- for attribute in vertex_input.attributes %}
    @location({{ attribute.location }}) {{ attribute.name }}: {{ attribute.type }},
    {%- endfor %}
}
