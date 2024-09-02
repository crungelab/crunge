{%- for binding in bindings %}
@group({{ binding.group }}) @binding( {{ binding.index }}) var {{binding.name}}: {{ binding.type }};
{%- endfor %}
