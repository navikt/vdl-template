{% macro ref(model_name) %}

  {% do return(builtins.ref(model_name).include(database=false)) %}

{% endmacro %}
