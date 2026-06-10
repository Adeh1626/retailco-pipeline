WITH source AS (
    SELECT
        id                        AS order_id,
        customer_id               AS customer_id,
        store_id                  AS store_id,
        employee_id               AS employee_id,
        status                    AS status,
        order_date::TIMESTAMPTZ   AS order_date,
        is_deleted::BOOLEAN       AS is_deleted,
        updated_at::TIMESTAMPTZ   AS updated_at
    FROM raw.orders
)
SELECT * FROM source
