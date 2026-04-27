# 🚀 User Activity Analytics Platform

End-to-end **data pipeline + analytics platform** that simulates user clickstream data, processes it via ETL, and computes core product KPIs: **DAU, Retention, and Conversion Funnel** — with a **Streamlit dashboard** for visualization.

---

## 📌 Problem

Product teams lack quick visibility into:
- Daily engagement (DAU)
- Retention (who comes back)
- Funnel drop-offs (where users churn)

This project builds a **pipeline + SQL analytics + dashboard** to answer these.

---

## 🧱 Architecture
Python (Data Generation)
↓
CSV (Raw Data)
↓
ETL (extract.py → load.py)
↓
PostgreSQL (events_raw)
↓
SQL (DAU, Retention, Funnel)
↓
Streamlit Dashboard


---

## ⚙️ Tech Stack

- **Python** (Pandas, NumPy, SQLAlchemy)
- **PostgreSQL**
- **SQL**
- **Streamlit**
- **Matplotlib**

---

## 📊 KPIs

### DAU (Daily Active Users)
Unique users active per day.

### Retention (Day 1 Cohort)
% of users returning the next day after signup.

### Conversion Funnel
Includes:
- Signup → Login %
- Login → Purchase %

---

## ⚡ Highlights

- Built modular **ETL pipeline**
- Simulated **10,000+ events**
- Fixed incorrect **event-level metrics** using **user-level aggregation**
- Wrote SQL for **cohort + funnel analysis**
- Delivered interactive **Streamlit dashboard**

---

## 📈 Dashboard

- KPI Cards (Total Users, Avg DAU, Max DAU)
- DAU trend chart
- Funnel visualization
- Retention table + trend

---

## 🚀 Run Locally

### 1. Clone
```bash
git clone <your-repo-link>
cd user-activity-pipeline
