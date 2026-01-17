import pandas as pd
import numpy as np

# 1. Load the clean logs
df = pd.read_csv("game_admin_logs.csv")
df['timestamp'] = pd.to_datetime(df['timestamp']) # Convert text to Date Objects

print(f"Loaded {len(df)} logs.")

# --- FEATURE 1: TIME OF DAY ---
# Simple: Just extract the hour (0-23)
df['hour_of_day'] = df['timestamp'].dt.hour
print("Feature 'hour_of_day' created.")

# --- FEATURE 2: SPEED (Actions Per Second) ---
# This is tricky. We need the time difference between THIS action and the PREVIOUS action
# for the SAME admin.

# Sort by admin and time to be safe
df = df.sort_values(['admin_id', 'timestamp'])

# Calculate time difference in seconds
# GroupBy ensures we don't calculate diff between Admin_1's last action and Admin_2's first action.
df['time_diff'] = df.groupby('admin_id')['timestamp'].diff().dt.total_seconds()

# Fill the first action (NaN) with a reasonable default (e.g., 60 seconds)
df['time_diff'] = df['time_diff'].fillna(60.0)

# Avoid division by zero (if actions happen at exact same second)
df['time_diff'] = df['time_diff'].replace(0, 1)

# Actions Per Minute (Example: 1 action / 60 seconds = 0.016 APM)
# If time_diff is small (1 sec), APM is high (60).
df['actions_per_min'] = 60 / df['time_diff']
print("Feature 'actions_per_min' created.")

# --- FEATURE 3: NEW IP ADDRESS? ---
# We want to know: "Has this Admin used this IP before?"

# Create a list of "Known IPs" for each admin based on their history.
# For this simple version, we'll mark it as "Suspicious" if it's NOT their most common IP.

# Find the "Mode" (Most frequent) IPs for each admin
common_ips = df.groupby('admin_id')['ip_address'].agg(lambda x:(pd.Series.mode(x))).to_dict()

# Create a function to check
def is_rare_ip(row):
    admin = row['admin_id']
    ip = row['ip_address']
    # If the IP is different from their "Home" IP, return 1 (True), else 0 (False)
    if ip not in common_ips[admin]:
        return 1
    return 0

df['is_rare_ip'] = df.apply(is_rare_ip, axis=1)
print("Feature 'is_rare_ip' created.")

# --- FINALIZE ---
# We only want the NUMBERS for the model.
# We keep the original columns for reference, but save a clean feature set.

features = df[['hour_of_day', 'actions_per_min', 'is_rare_ip']]

# Save full dataset with features
df.to_csv("game_admin_derived.csv", index=False)
print("Saved derived data fields to 'game_admin_derived.csv'.")
features.to_csv("game_admin_features.csv", index=False)
print("Saved features to 'game_admin_features.csv'.")