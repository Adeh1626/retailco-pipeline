SELECT
    MD5(customer_id || updated_at::TEXT)  AS customer_key,
    customer_id,
    customer_name,
    email,
    segment,
    address,
    city,
    is_deleted,
    updated_at                            AS valid_from,
    NULL::TIMESTAMPTZ                     AS valid_to,
    TRUE                                  AS is_current
FROM {{ ref('stg_customers') }}