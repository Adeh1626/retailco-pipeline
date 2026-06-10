WITH source AS (
    SELECT
        id                           AS movement_id,
        product_id                   AS product_id,
        store_id                     AS store_id,
        movement_type                AS movement_type,
        quantity::INT                AS quantity,
        movement_date::TIMESTAMPTZ   AS movement_date,
        updated_at::TIMESTAMPTZ      AS updated_at
    FROM raw.inventory_movements
)
SELECT * FROM source