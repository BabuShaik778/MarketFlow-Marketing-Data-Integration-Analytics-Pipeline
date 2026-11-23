-- 1. CTR and CPC by campaign and week.
SELECT strftime('%Y-%W', a.spend_date) AS week,
       c.campaign_name,
       1.0 * SUM(a.clicks) / NULLIF(SUM(a.impressions), 0) AS ctr,
       SUM(a.spend_inr) / NULLIF(SUM(a.clicks), 0) AS cpc
FROM fact_ad_spend_daily a
JOIN dim_campaign c ON c.campaign_id = a.campaign_id
GROUP BY week, c.campaign_name;

-- 2. Order-item value by campaign platform (simplified attribution example).
SELECT c.platform, SUM(oi.quantity * oi.unit_price_inr) AS item_value
FROM fact_order_item oi
JOIN fact_order o ON o.order_id = oi.order_id
JOIN fact_lead l ON l.customer_id = o.customer_id
JOIN dim_campaign c ON c.campaign_id = l.campaign_id
WHERE o.status NOT IN ('cancelled', 'returned')
GROUP BY c.platform;

-- 3. Lead-to-order funnel.
SELECT COUNT(DISTINCT l.lead_id) AS leads,
       COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN l.lead_id END) AS leads_with_orders
FROM fact_lead l
LEFT JOIN fact_order o
  ON o.customer_id = l.customer_id AND o.order_date >= l.created_at;

-- 4. Latest lead before each order.
SELECT o.order_id, o.customer_id, o.order_date, l.lead_id, l.campaign_id
FROM fact_order o
LEFT JOIN fact_lead l ON l.lead_id = (
    SELECT l2.lead_id FROM fact_lead l2
    WHERE l2.customer_id = o.customer_id AND l2.created_at <= o.order_date
    ORDER BY l2.created_at DESC LIMIT 1
);

-- 5. Daily spend running total and 7-row moving average.
WITH daily AS (
    SELECT spend_date, SUM(spend_inr) AS spend
    FROM fact_ad_spend_daily GROUP BY spend_date
)
SELECT spend_date, spend,
       SUM(spend) OVER (ORDER BY spend_date) AS running_spend,
       AVG(spend) OVER (ORDER BY spend_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg
FROM daily ORDER BY spend_date;

-- 6. Potential repeated customer/campaign leads.
SELECT customer_id, campaign_id, COUNT(*) AS lead_count
FROM fact_lead GROUP BY customer_id, campaign_id
HAVING COUNT(*) > 1;

-- 7. Revenue by product.
SELECT p.product_name, SUM(oi.quantity * oi.unit_price_inr) AS revenue_before_gst
FROM fact_order_item oi
JOIN dim_product p ON p.product_id = oi.product_id
GROUP BY p.product_name ORDER BY revenue_before_gst DESC;

-- 8. Monthly spend and sales value. This is not attribution-safe ROAS.
WITH spend AS (
    SELECT substr(spend_date, 1, 7) AS month, SUM(spend_inr) AS ad_spend
    FROM fact_ad_spend_daily GROUP BY substr(spend_date, 1, 7)
),
sales AS (
    SELECT substr(o.order_date, 1, 7) AS month,
           SUM(oi.quantity * oi.unit_price_inr) AS sales_value
    FROM fact_order o JOIN fact_order_item oi ON oi.order_id = o.order_id
    WHERE o.status NOT IN ('cancelled', 'returned')
    GROUP BY substr(o.order_date, 1, 7)
)
SELECT spend.month, spend.ad_spend, sales.sales_value,
       sales.sales_value / NULLIF(spend.ad_spend, 0) AS simple_roas
FROM spend LEFT JOIN sales ON sales.month = spend.month;
