WITH source AS (
    SELECT
        id                          AS payment_id,
        order_id                    AS order_id,
        payment_method_id           AS payment_method_id,
        amount_paid::NUMERIC        AS amount_paid,
        is_refund::BOOLEAN          AS is_refund,
        updated_at::TIMESTAMPTZ     AS updated_at
    FROM raw.payments
)
SELECT * FROM source