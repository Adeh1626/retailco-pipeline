SELECT
    MD5(store_id)    AS store_key,
    store_id,
    store_name,
    city,
    region,
    is_deleted
FROM {{ ref('stg_stores') }}