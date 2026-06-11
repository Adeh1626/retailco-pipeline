SELECT
    MD5(customer_id || dbt_updated_at::TEXT) AS customer_key,
    customer_id,
    customer_name,
    email,
    segment,
    address,
    city,
    is_deleted,
    dbt_valid_from   AS valid_from,
    dbt_valid_to     AS valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END AS is_current
FROM {{ ref('snap_customers') }}