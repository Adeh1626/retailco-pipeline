SELECT
    payment_id,
    order_id,
    amount_paid,
    CASE
        WHEN amount_paid = 0     THEN 'zero_amount'
        WHEN amount_paid < 0
         AND is_refund = FALSE   THEN 'unexplained_negative'
        ELSE 'other'
    END                          AS flag_reason,
    NOW()                        AS flagged_at
FROM {{ ref('stg_payments') }}
WHERE amount_paid = 0
   OR (amount_paid < 0 AND is_refund = FALSE)