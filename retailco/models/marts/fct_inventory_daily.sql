SELECT
    MD5(product_id || store_id || movement_date::DATE::TEXT) AS inventory_key,
    TO_CHAR(movement_date::DATE, 'YYYYMMDD')::INT            AS date_key,
    MD5(product_id)                                          AS product_key,
    MD5(store_id)                                            AS store_key,
    SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END)     AS quantity_in,
    SUM(CASE WHEN quantity < 0 THEN ABS(quantity) ELSE 0 END) AS quantity_out,
    SUM(quantity)                                             AS net_quantity
FROM {{ ref('stg_inventory_movements') }}
GROUP BY product_id, store_id, movement_date::DATE