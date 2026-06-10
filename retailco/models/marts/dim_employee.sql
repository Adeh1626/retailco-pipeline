SELECT
    MD5(employee_id)  AS employee_key,
    employee_id,
    employee_name,
    role,
    store_id,
    is_deleted
FROM {{ ref('stg_employees') }}