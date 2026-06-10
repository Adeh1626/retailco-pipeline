SELECT
    MD5(payment_method_id)  AS payment_method_key,
    payment_method_id,
    method_name,
    is_deleted
FROM {{ ref('stg_payment_methods') }}