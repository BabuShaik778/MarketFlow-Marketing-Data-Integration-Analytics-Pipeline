-- Duplicate lead IDs (the primary key should prevent these).
SELECT lead_id, COUNT(*) FROM fact_lead GROUP BY lead_id HAVING COUNT(*) > 1;

-- Status values that are not normalized.
SELECT lead_id, status FROM fact_lead WHERE status <> lower(trim(status));

-- Invalid negative advertising spend.
SELECT * FROM fact_ad_spend_daily WHERE spend_inr < 0;

-- Clicks should not exceed impressions.
SELECT * FROM fact_ad_spend_daily WHERE clicks > impressions;

-- Order statuses to review.
SELECT status, COUNT(*) FROM fact_order GROUP BY status;

-- Rejected rows grouped by source and reason.
SELECT source_name, reason, COUNT(*) AS total
FROM rejected_rows GROUP BY source_name, reason ORDER BY total DESC;
