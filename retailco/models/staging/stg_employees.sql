WITH source AS (
    SELECT
        id                      AS employee_id,
        name                    AS employee_name,
        role                    AS role,
        store_id                AS store_id,
        is_deleted::BOOLEAN     AS is_deleted,
        updated_at::TIMESTAMPTZ AS updated_at
    FROM raw.employees
)
SELECT * FROM source