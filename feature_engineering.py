import pandas as pd
import numpy as np

df = pd.read_csv("game_admin_logs.csv")
df['timestamp'] = pd.to_datetime(df['timestamp']) # Convert text to Date Objects

print(f"Loaded {len(df)} logs.")

# --- FEATURE 1: TIME OF DAY ---
df['hour_of_day'] = df['timestamp'].dt.hour
print("Feature 'hour_of_day' created.")

# --- FEATURE 2: SPEED (Actions Per Second) ---
df = df.sort_values(['admin_id', 'timestamp'])
df['time_diff'] = df.groupby('admin_id')['timestamp'].diff().dt.total_seconds()
df['time_diff'] = df['time_diff'].fillna(9999999) # Fill the first action (NaN) with a high value so that the actions_per_second is essentially 0 but not exactly 0
df['time_diff'] = df['time_diff'].replace(0, 1) #Avoiding division by zero, which is highly unlikely but is still a non-zero possibility

# Actions Per Minute
df['actions_per_min'] = 60 / df['time_diff']
print("Feature 'actions_per_min' created.")

# --- FEATURE 3: NEW IP ADDRESS? ---
common_ips = df.groupby('admin_id')['ip_address'].agg(lambda x:(pd.Series.mode(x))).to_dict()

def is_rare_ip(row):
    admin = row['admin_id']
    ip = row['ip_address']
    if ip not in common_ips[admin]: # If the IP is different from their IP, return 1 (True), else 0 (False)
        return 1
    return 0

df['is_rare_ip'] = df.apply(is_rare_ip, axis=1)
print("Feature 'is_rare_ip' created.")


features = df[['hour_of_day', 'actions_per_min', 'is_rare_ip']]
df.to_csv("game_admin_derived.csv", index=False)
print("Saved derived data fields to 'game_admin_derived.csv'.")
features.to_csv("game_admin_features.csv", index=False)
print("Saved features to 'game_admin_features.csv'.")
