# RetailCo Business Insights Report

## Overview
This report answers five key business questions using data extracted from
the RetailCo ERP system, processed through our data pipeline, and modelled
into analytics-ready tables in the warehouse.

---

## 1. Revenue Performance

| Store | Total Revenue (₦) | Total Orders |
|---|---|---|
| RetailCo Kano | 41,484,185 | 274 |
| RetailCo Lagos | 39,875,944 | 265 |
| RetailCo Port Harcourt | 39,721,920 | 271 |
| RetailCo Abuja | 37,025,502 | 272 |

**Key Finding:** Kano is the top performing store with ₦41.5M in revenue
despite not being the largest city. All four stores perform within a similar
range (₦37M–₦41.5M), suggesting consistent operations across locations.
Abuja trails slightly and may benefit from targeted promotions.

---

## 2. Customer Behaviour

| Segment | Customers | Avg Order Value (₦) | Total Purchases |
|---|---|---|---|
| Premium | 62 | 152,769 | 392 |
| Occasional | 61 | 142,084 | 366 |
| Regular | 50 | 142,651 | 324 |

**Key Finding:** Premium customers spend the most per order (₦152,769)
and make the most purchases. Interestingly, occasional customers outnumber
regular customers, suggesting many buyers shop infrequently. A loyalty
programme targeting occasional customers could convert them to regulars
and significantly increase revenue.

---

## 3. Product & Discount Analysis

| Category | Revenue (₦) | Discounts (₦) | Discount Rate |
|---|---|---|---|
| Electronics | 47,060,779 | 868,740 | 1.85% |
| Home | 40,353,419 | 761,592 | 1.89% |
| Food | 33,185,404 | 560,020 | 1.69% |
| Beauty | 25,540,301 | 478,997 | 1.88% |
| Clothing | 11,967,649 | 237,672 | 1.99% |

**Key Finding:** Electronics is the top revenue category at ₦47M.
Discount rates are consistently low across all categories (1.7–2.0%),
meaning discounting has minimal margin impact. Clothing has the lowest
revenue but the highest discount rate — worth investigating whether
increased discounting could drive volume.

---

## 4. Payment Channel Insights

| Method | Transactions | Total Amount (₦) | Refunds |
|---|---|---|---|
| Cash | 135 | 5,370,876 | 9 |
| Mobile Money | 126 | 5,844,949 | 10 |
| Card | 124 | 5,578,782 | 3 |
| Bank Transfer | 99 | 4,237,430 | 5 |

**Key Finding:** Cash remains the most used payment method by transaction
count, reflecting Nigerian retail norms. However, mobile money generates
the highest total value despite fewer transactions, suggesting higher-value
purchases via mobile. Card payments have the fewest refunds (only 3),
making it the most reliable channel. Bank transfers are least used and
may have friction in the checkout process.

---

## 5. Data Quality

| Flag Reason | Count |
|---|---|
| Zero Amount | 17 |

**Key Finding:** 17 payments were flagged as anomalous due to zero amounts.
These have been quarantined in the flagged_payments table and excluded from
all revenue calculations. No unexplained negative payments were detected.
The pipeline's data quality checks are working correctly.

---

## Summary Recommendations

1. **Investigate Abuja underperformance** — smallest revenue despite being
   the capital city.
2. **Launch occasional-to-regular conversion programme** — large pool of
   occasional buyers represents significant revenue opportunity.
3. **Promote mobile money** — highest transaction value, growing adoption.
4. **Review Clothing category** — lowest revenue, highest discount rate.
5. **Investigate zero-amount payments** — 17 flagged transactions need
   review with the finance team.