{% snapshot snap_customers %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at',
    )
}}

SELECT * FROM {{ ref('stg_customers') }}

{% endsnapshot %}