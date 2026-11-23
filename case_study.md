# ROAS discrepancy case study

Dashboard: ₹84 lakh revenue / ₹20 lakh spend = 4.2x.
Finance: ₹65 lakh revenue / ₹25 lakh spend = 2.6x.
ROAS is eligible attributed revenue divided by eligible advertising spend.

## Investigation
1. Agree on reporting dates, timezone, currency and attribution definition.
2. Verify every advertising API page. `has_next=true` means more pages remain.
3. Compare API versions and page-size settings, recording request metadata.
4. Reconcile spend by platform and date. Retry HTTP 429 errors safely without
   double-counting successful records.
5. Exclude cancelled and returned orders if required by the finance definition.
6. Prevent join fan-out by selecting one eligible lead attribution per order.

## Arithmetic
84 / 20 = 4.2x; 65 / 25 = 2.6x.
The dashboard has ₹19 lakh more reported revenue and ₹5 lakh less reported spend.
Investigate the revenue and spend differences separately.

If 4,520 joined rows represent 4,120 distinct orders, there are 400 extra rows.
At ₹2,500 average value, the possible overstatement is ₹10 lakh. This is only
an estimate; identify duplicated order IDs and calculate their actual amounts.

## First 24 hours
- Preserve raw API responses and existing reports.
- Re-fetch every page and record page/version metadata.
- Reconcile daily spend by platform.
- Rebuild revenue from distinct eligible order IDs.
- Apply the agreed attribution rule and compare totals with Finance.
- Publish only after order-level controls pass.

## Alerts
- Incomplete pagination.
- Missing API pages or unexpected source row counts.
- Duplicate order IDs in revenue aggregation.
- Cancelled/returned orders included in eligible revenue.
- Negative spend or clicks greater than impressions.
- Daily source-to-database spend variance.
- Failed or unusually long pipeline runs.

## Example leadership update
The 4.2x dashboard result is not yet comparable with Finance's 2.6x result.
Current evidence suggests incomplete advertising extraction and possible
revenue inflation from order-to-lead join fan-out. Cancelled and returned orders
and spend reconciliation also need verification. We are rebuilding the period
from raw records with one documented attribution and net-revenue definition.
We will share an order-level reconciliation before confirming final ROAS.
Until then, avoid increasing budgets based only on the 4.2x dashboard figure.

## Architecture
A scheduled Python batch job is sufficient for a small daily pipeline. Airflow
is useful when many dependent jobs need orchestration, retries and backfills.
SQLite is suitable for this local exercise; MySQL or PostgreSQL is better for
a multi-user application. Use streaming only when low-latency data is required.
Restrict personal-data access and require human approval before automated
systems change production records.
