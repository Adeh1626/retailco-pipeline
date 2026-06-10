WITH source AS (
    SELECT
        id                      AS store_id,
        name                    AS store_name,
        city                    AS city,
        region                  AS region,
        is_deleted::BOOLEAN     AS is_deleted,
        updated_at::TIMESTAMPTZ AS updated_at
    FROM raw.stores
)
SELECT * FROM source