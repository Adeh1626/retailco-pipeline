SELECT
    MD5(product_id || updated_at::TEXT)  AS product_key,
    product_id,
    product_name,
    category,
    price,
    is_deleted,
    updated_at                           AS valid_from,
    NULL::TIMESTAMPTZ                    AS valid_to,
    TRUE                                 AS is_current
FROM {{ ref('stg_products') }}