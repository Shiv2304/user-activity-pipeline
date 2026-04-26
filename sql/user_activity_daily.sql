-- Daily user activity aggregation query placeholder
SELECT
    user_id,
    DATE(activity_timestamp) AS activity_date,
    COUNT(*) AS event_count
FROM user_activity_events
GROUP BY user_id, DATE(activity_timestamp);
