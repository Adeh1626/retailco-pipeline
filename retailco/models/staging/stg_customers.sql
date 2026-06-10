WITH source AS (
    SELECT
        id                      AS customer_id,
        name                    AS customer_name,
        email                   AS email,
        segment                 AS segment,
        address                 AS address,
        city                    AS city,
        is_deleted::BOOLEAN     AS is_deleted,
        updated_at::TIMESTAMPTZ AS updated_at,
        effective_from::TIMESTAMPTZ AS effective_from
    FROM raw.customers
)
SELECT * FROM source