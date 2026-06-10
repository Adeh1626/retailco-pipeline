WITH date_spine AS (
    SELECT generate_series(
        '2022-01-01'::DATE,
        '2025-12-31'::DATE,
        '1 day'::INTERVAL
    )::DATE AS full_date
)
SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::INT          AS date_key,
    full_date,
    EXTRACT(YEAR FROM full_date)::INT             AS year,
    EXTRACT(QUARTER FROM full_date)::INT          AS quarter,
    EXTRACT(MONTH FROM full_date)::INT            AS month,
    TO_CHAR(full_date, 'Month')                   AS month_name,
    EXTRACT(WEEK FROM full_date)::INT             AS week,
    EXTRACT(DOW FROM full_date)::INT              AS day_of_week,
    TO_CHAR(full_date, 'Day')                     AS day_name,
    CASE WHEN EXTRACT(DOW FROM full_date) IN (0,6)
         THEN TRUE ELSE FALSE END                 AS is_weekend,
    CASE WHEN TO_CHAR(full_date, 'MM-DD') IN (
        '01-01', '05-01', '10-01', '12-25', '12-26'
    ) THEN TRUE ELSE FALSE END                    AS is_public_holiday
FROM date_spine