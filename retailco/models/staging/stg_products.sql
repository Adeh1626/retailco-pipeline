WITH source AS (
    SELECT
        id                          AS product_id,
        name                        AS product_name,
        category                    AS category,
        price::NUMERIC              AS price,
        is_deleted::BOOLEAN         AS is_deleted,
        updated_at::TIMESTAMPTZ     AS updated_at,
        effective_from::TIMESTAMPTZ AS effective_from
    FROM raw.products
)
SELECT * FROM source