{%- for assignment in assignments %}
output.{{ assignment.name }} = {{ assignment.value }};
{%- endfor %}
