WITH source AS (
    SELECT
        id                      AS payment_method_id,
        method_name             AS method_name,
        is_deleted::BOOLEAN     AS is_deleted,
        updated_at::TIMESTAMPTZ AS updated_at
    FROM raw.payment_methods
)
SELECT * FROM source