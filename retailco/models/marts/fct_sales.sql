WITH order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),
orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
dim_customer AS (
    SELECT * FROM {{ ref('dim_customer') }}
    WHERE is_current = TRUE
),
dim_product AS (
    SELECT * FROM {{ ref('dim_product') }}
    WHERE is_current = TRUE
),
dim_store AS (
    SELECT * FROM {{ ref('dim_store') }}
),
dim_employee AS (
    SELECT * FROM {{ ref('dim_employee') }}
)
SELECT
    MD5(oi.order_item_id)                         AS sales_key,
    oi.order_item_id,
    oi.order_id,
    TO_CHAR(o.order_date, 'YYYYMMDD')::INT        AS date_key,
    dc.customer_key,
    dp.product_key,
    ds.store_key,
    de.employee_key,
    oi.quantity,
    oi.unit_price,
    oi.discount_amount,
    (oi.quantity * oi.unit_price) - oi.discount_amount AS line_total
FROM order_items oi
LEFT JOIN orders o          ON oi.order_id      = o.order_id
LEFT JOIN dim_customer dc   ON o.customer_id    = dc.customer_id
LEFT JOIN dim_product dp    ON oi.product_id    = dp.product_id
LEFT JOIN dim_store ds      ON o.store_id       = ds.store_id
LEFT JOIN dim_employee de   ON o.employee_id    = de.employee_id
WHERE dc.is_deleted = FALSE
  AND dp.is_deleted = FALSE