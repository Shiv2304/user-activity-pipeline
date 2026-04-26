import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("your_connection_string")

df = pd.read_sql("SELECT * FROM events_raw", engine)

dau = df.groupby(df['event_timestamp'].dt.date)['user_id'].nunique()

print(dau.head())