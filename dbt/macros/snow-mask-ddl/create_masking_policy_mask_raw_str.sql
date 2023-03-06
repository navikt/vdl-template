{% macro create_masking_policy_mask_raw_str(node_database,node_schema) %}

CREATE MASKING POLICY IF NOT EXISTS  {{node_database}}.{{node_schema}}.mask_raw_str AS (val STRING) 
  RETURNS STRING ->
      CASE WHEN CURRENT_ROLE() IN ('<PROJECT_TRANSFORMER>','<PROJECT_LOADER>' ) THEN val 
      ELSE NULL
      END 

{% endmacro %}