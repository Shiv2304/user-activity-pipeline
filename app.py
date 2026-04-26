import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import matplotlib.pyplot as plt

# ------------------ DB CONNECTION ------------------
connection_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Shivam@23",
    host="localhost",
    port=5432,
    database="olist"
)

engine = create_engine(connection_url)

# ------------------ TITLE ------------------
st.title("User Activity Analytics Platform")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Filters")
st.sidebar.write("Dataset: Last 30 Days")

# ------------------ DAU ------------------
st.header("Daily Active Users")

dau_query = """
SELECT DATE(event_timestamp) AS date,
COUNT(DISTINCT user_id) AS dau
FROM events_raw
GROUP BY date
ORDER BY date;
"""
dau_df = pd.read_sql(dau_query, engine)

# KPI CARDS
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", dau_df['dau'].sum())
col2.metric("Avg DAU", int(dau_df['dau'].mean()))
col3.metric("Max DAU", int(dau_df['dau'].max()))

# GRAPH
st.line_chart(dau_df.set_index("date"))

# INSIGHT
st.info(f"""
Average DAU is {int(dau_df['dau'].mean())}, with peak usage reaching {int(dau_df['dau'].max())}.
User activity appears stable with moderate daily variation.
""")

st.markdown("---")

# ------------------ FUNNEL ------------------
st.header("Conversion Funnel")

funnel_query = """
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
    COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 THEN 1 END) AS login,
    COUNT(CASE WHEN signed_up = 1 AND logged_in = 1 AND purchased = 1 THEN 1 END) AS purchase
FROM users;
"""
funnel_df = pd.read_sql(funnel_query, engine)

# BAR CHART
values = funnel_df.iloc[0]
labels = ["Signups", "Login", "Purchase"]
data = [values['signups'], values['login'], values['purchase']]

fig, ax = plt.subplots()
ax.bar(labels, data)
st.pyplot(fig)

st.markdown("---")

# ------------------ RETENTION ------------------
st.header("User Retention Analysis")

retention_query = """
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
"""
retention_df = pd.read_sql(retention_query, engine)

# TABLE
st.dataframe(retention_df)

# GRAPH
st.line_chart(retention_df.set_index("signup_date")["retention_rate"])

# INSIGHT
avg_retention = retention_df['retention_rate'].mean()

st.info(f"""
Average Day 1 retention is {round(avg_retention,2)}%.
Indicates moderate user engagement and repeat usage.
""")