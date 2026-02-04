import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(0)

# --- CONFIGURATION ---
NUM_ADMINS = 5
NUM_DAYS = 30
AVG_ACTIONS_PER_DAY = 50
FILENAME = "game_admin_logs.csv"

# Admin Profiles
admins = [f"admin_{i}" for i in range(1, NUM_ADMINS + 1)]
ips = {admin: fake.ipv4() for admin in admins}

# The work actions an admin can perform
work_actions = ['view_player_profile', 'ban_player', 'unban_player', 'reset_password', 'modify_currency']
work_weights = [0.60, 0.05, 0.05, 0.25, 0.05] #Should all add up to 1

data = []

# --- GENERATE NORMAL TRAFFIC ---
start_date = datetime(2024, 1, 1)
print("Generating normal traffic (Sequential Sessions)...")
for day in range(NUM_DAYS):
    current_date = start_date + timedelta(days=day)

    for admin in admins:
        if random.random() > 0.1: # 90% chance to work today
            num_actions = np.random.poisson(AVG_ACTIONS_PER_DAY)

            # Start work around 2 PM (14:00) +/- 2 hours
            start_hour = int(np.random.normal(14, 2))
            start_minute = np.random.randint(0, 60)
            start_hour = max(0, min(23, start_hour))  # Safety clamp

            session_start_time = current_date.replace(hour=start_hour, minute=start_minute, second=0)
            current_session_ip = ips[admin] if random.random() > 0.01 else fake.ipv4() # Use the same IP for the entire session
            current_time = session_start_time # We use this variable to track time moving forward

            for i in range(num_actions):
                time_step = np.random.randint(10, 120)
                current_time += timedelta(seconds=time_step) #A gap of 10 to 120 seconds between each action
                if i == 0:
                    action = 'login'
                elif i == num_actions - 1:
                    action = 'logout'
                else:
                    action = np.random.choice(work_actions, p=work_weights)

                data.append({
                    "timestamp": current_time,
                    "admin_id": admin,
                    "action": action,
                    "ip_address": current_session_ip,
                    "status": "Success"
                })

# --- INJECT ATTACKS (Keep these the same) ---
print("Injecting attacks...")

# Scenario 1: The "R6 Siege" Hack
hacker_time = start_date + timedelta(days=15)
hacker_time = hacker_time.replace(hour=3, minute=0, second=0)

for i in range(200):
    data.append({
        "timestamp": hacker_time + timedelta(seconds=i * 3),
        "admin_id": "admin_1",
        "action": "ban_player",
        "ip_address": fake.ipv4(),
        "status": "Success"
    })

# Scenario 2: Brute Force (Modified to allow 'login' failure)
bf_time = start_date + timedelta(days=5)
for i in range(20):
    data.append({
        "timestamp": bf_time + timedelta(seconds=i * 10),
        "admin_id": "admin_3",
        "action": "login",
        "ip_address": "192.168.1.50",
        "status": "Fail"
    })
# Successful login
data.append({
    "timestamp": bf_time + timedelta(seconds=210),
    "admin_id": "admin_3",
    "action": "login",
    "ip_address": "192.168.1.50",
    "status": "Success"
})

# --- FINALIZE ---
df = pd.DataFrame(data)
df = df.sort_values("timestamp")
df.to_csv(FILENAME, index=False)
print(f"Successfully created {FILENAME} with {len(df)} logs.")