-- DAU
SELECT 
    DATE(event_timestamp) AS date,
    COUNT(DISTINCT user_id) AS dau
FROM events_raw
GROUP BY date
ORDER BY date;

--------------------------------------------------

-- RETENTION (Day 1)
SELECT 
    s.signup_date,
    COUNT(DISTINCT s.user_id) AS total_users,
    COUNT(DISTINCT a.user_id) AS retained_users,
    ROUND(
        COUNT(DISTINCT a.user_id) * 100.0 / COUNT(DISTINCT s.user_id), 2
    ) AS retention_rate
FROM (
    SELECT user_id, DATE(event_timestamp) AS signup_date
    FROM events_raw
    WHERE event_type = 'signup'
) s
LEFT JOIN (
    SELECT user_id, DATE(event_timestamp) AS activity_date
    FROM events_raw
) a
ON s.user_id = a.user_id
AND a.activity_date = s.signup_date + INTERVAL '1 day'
GROUP BY s.signup_date
ORDER BY s.signup_date;

--------------------------------------------------

-- FUNNEL (USER LEVEL)
WITH users AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'signup' THEN 1 ELSE 0 END) AS signed_up,
        MAX(CASE WHEN event_type = 'login' THEN 1 ELSE 0 END) AS logged_in,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events_raw
    GROUP BY user_id
)
SELECT
    COUNT(CASE WHEN signed_up = 1 THEN 1 END) AS signups,
    COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 THEN 1 END) AS signup_to_login,
    COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 AND purchased = 1 THEN 1 END) AS signup_to_purchase,

    ROUND(
        COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 THEN 1 END) * 100.0 /
        COUNT(CASE WHEN signed_up = 1 THEN 1 END), 2
    ) AS signup_to_login_pct,

    ROUND(
        COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 AND purchased = 1 THEN 1 END) * 100.0 /
        COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 THEN 1 END), 2
    ) AS login_to_purchase_pct
FROM users;