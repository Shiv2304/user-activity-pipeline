import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Ensure folder exists
os.makedirs("data/raw", exist_ok=True)

NUM_USERS = 1000
NUM_EVENTS = 10000

event_types = ["signup", "login", "purchase"]
features = ["home", "search", "product_page", "cart", "checkout"]

data = []
start_date = datetime.now() - timedelta(days=30)

for _ in range(NUM_EVENTS):
    user_id = random.randint(1, NUM_USERS)
    event_type = random.choices(event_types, weights=[0.1, 0.7, 0.2])[0]
    timestamp = start_date + timedelta(minutes=random.randint(0, 60*24*30))
    feature = random.choice(features)

    data.append([user_id, event_type, timestamp, feature])

df = pd.DataFrame(data, columns=["user_id", "event_type", "event_timestamp", "feature"])

df.to_csv("data/raw/events.csv", index=False)

print("Data generated successfully.")