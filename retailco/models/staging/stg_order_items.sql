WITH source AS (
    SELECT
        id                        AS order_item_id,
        order_id                  AS order_id,
        product_id                AS product_id,
        quantity::INT             AS quantity,
        unit_price::NUMERIC       AS unit_price,
        discount_amount::NUMERIC  AS discount_amount,
        updated_at::TIMESTAMPTZ   AS updated_at
    FROM raw.order_items
)
SELECT * FROM source