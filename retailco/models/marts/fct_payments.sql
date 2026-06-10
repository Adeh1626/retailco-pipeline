WITH payments AS (
    SELECT * FROM {{ ref('stg_payments') }}
    WHERE NOT (amount_paid = 0
           OR (amount_paid < 0 AND is_refund = FALSE))
),
orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
dim_customer AS (
    SELECT * FROM {{ ref('dim_customer') }}
    WHERE is_current = TRUE
),
dim_store AS (
    SELECT * FROM {{ ref('dim_store') }}
),
dim_payment_method AS (
    SELECT * FROM {{ ref('dim_payment_method') }}
)
SELECT
    MD5(p.payment_id)                        AS payment_key,
    p.payment_id,
    p.order_id,
    TO_CHAR(p.updated_at, 'YYYYMMDD')::INT   AS date_key,
    dc.customer_key,
    ds.store_key,
    dpm.payment_method_key,
    p.amount_paid,
    p.is_refund
FROM payments p
LEFT JOIN orders o          ON p.order_id           = o.order_id
LEFT JOIN dim_customer dc   ON o.customer_id        = dc.customer_id
LEFT JOIN dim_store ds      ON o.store_id           = ds.store_id
LEFT JOIN dim_payment_method dpm
                            ON p.payment_method_id  = dpm.payment_method_id