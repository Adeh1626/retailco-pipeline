SELECT
    MD5(product_id || dbt_updated_at::TEXT) AS product_key,
    product_id,
    product_name,
    category,
    price,
    is_deleted,
    dbt_valid_from   AS valid_from,
    dbt_valid_to     AS valid_to,
    CASE WHEN dbt_valid_to IS NULL THEN TRUE ELSE FALSE END AS is_current
FROM {{ ref('snap_products') }}