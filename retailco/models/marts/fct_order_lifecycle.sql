SELECT
    MD5(order_id)                                           AS order_key,
    order_id,
    TO_CHAR(order_date, 'YYYYMMDD')::INT                    AS date_key,
    MD5(customer_id)                                        AS customer_key,
    MD5(store_id)                                           AS store_key,
    MD5(employee_id)                                        AS employee_key,
    status                                                  AS current_status,
    CASE WHEN status = 'pending'
         THEN order_date END                                AS pending_at,
    CASE WHEN status = 'paid'
         THEN updated_at END                                AS paid_at,
    CASE WHEN status = 'shipped'
         THEN updated_at END                                AS shipped_at,
    CASE WHEN status = 'delivered'
         THEN updated_at END                                AS delivered_at,
    CASE WHEN status = 'cancelled'
         THEN updated_at END                                AS cancelled_at
FROM {{ ref('stg_orders') }}