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

# Admin Profiles and IP addresses
admins = [f"admin_{i}" for i in range(1, NUM_ADMINS + 1)]
ips = {admin: fake.ipv4() for admin in admins}

# The work actions an admin can perform
work_actions = [
    "view_player_profile",
    "ban_player",
    "unban_player",
    "reset_password",
    "modify_currency",
]
work_weights = [0.60, 0.05, 0.05, 0.25, 0.05]  # Should all add up to 1


# --- ATTACKS ---
# Scenario 1: The "R6 Siege" Hack
def hack(admin, current_time):
    hacker_time = current_time

    if random.random() < 0.30:  # 30% chance that the attack is happening via the admin's actual IP address (leaked credentials, hacked or stolen laptop/PC)
        attacker_ip = ips[admin]
    else:
        attacker_ip = fake.ipv4()

    for i in range(random.randint(100, 150)): # Anywhere between, 100 to 150 ban_player actions
        step = random.randint(2, 10) # Anywhere between, 2 to 10 seconds between each ban
        hacker_time += timedelta(seconds=step)
        data.append(
            {
                "timestamp": hacker_time,
                "admin_id": admin,
                "action": "ban_player",
                "ip_address": attacker_ip,
                "status": "Success",
                "is_attack": 1,
            }
        )


# Scenario 2: Brute Force
def brute_force(admin, current_time):
    bf_time = random.choice(
        [current_time + timedelta(hours=7), current_time - timedelta(hours=7)]
    )
    attacker_ip = fake.ipv4()

    for i in range(random.randint(15, 25)):
        data.append(
            {
                "timestamp": bf_time + timedelta(seconds=i * 10),
                "admin_id": admin,
                "action": "login",
                "ip_address": attacker_ip,
                "status": "Fail",
                "is_attack": 1,
            }
        )
    # Successful login
    data.append(
        {
            "timestamp": bf_time + timedelta(seconds=random.randint(150, 250)),
            "admin_id": admin,
            "action": "login",
            "ip_address": attacker_ip,
            "status": "Success",
            "is_attack": 1,
        }
    )


data = []

# --- GENERATE NORMAL TRAFFIC ---
start_date = datetime(2024, 1, 1)
print("Generating normal traffic (Sequential Sessions)...")
for day in range(NUM_DAYS):
    current_date = start_date + timedelta(days=day)

    for admin in admins:
        if random.random() > 0.1:  # 90% chance to work today
            num_actions = np.random.poisson(AVG_ACTIONS_PER_DAY)

            # Start work around 2 PM (14:00) +/- 2 hours
            start_hour = int(np.random.normal(14, 2))
            start_minute = np.random.randint(0, 60)
            start_hour = max(0, min(23, start_hour))  # Safety clamp

            # 25% chance that an admin is working late/early hours
            early_late = False
            if random.random() <= 0.25:
                start_hour = random.choice([random.choice(range(19, 23)), random.choice(range(4, 7))]) # Working late hours between 7 and 11pm and early hours between 4 am and 7 am
                early_late = True

            session_start_time = current_date.replace(hour=start_hour, minute=start_minute, second=0)
            current_session_ip = (ips[admin] if random.random() > 0.01 else fake.ipv4())  # Use the same IP for the entire session
            current_time = session_start_time  # We use this variable to track time moving forward

            for i in range(num_actions):
                if random.random() < 0.1:  # 10% chance that an admin performs actions very fast which looks suspicious
                    time_step = np.random.randint(2, 10)
                else:
                    time_step = np.random.randint(10, 120)
                current_time += timedelta(seconds=time_step) # A gap of 10 to 120 seconds between each action
                if i == 0:
                    action = "login"
                elif i == num_actions - 1:
                    action = "logout"
                else:
                    action = np.random.choice(work_actions, p=work_weights)
                data.append(
                    {
                        "timestamp": current_time,
                        "admin_id": admin,
                        "action": action,
                        "ip_address": current_session_ip,
                        "status": "Success",
                        "is_attack": 0,
                    }
                )
                if early_late and random.random() < 0.15:  # 85% chance that the admin is actually working late/early and not a malicious attack
                    continue

            if random.random() <= 0.20:  # 20% chance that there will be malicious activity
                attack = random.choice([1, 2])
                if attack == 1:
                    hack(admin, current_time)
                elif attack == 2:
                    brute_force(admin, current_time)

# --- FINALIZE ---
df = pd.DataFrame(data)
df = df.sort_values("timestamp").sort_values("admin_id")
df.to_csv(FILENAME, index=False)
print(f"Successfully created {FILENAME} with {len(df)} logs.")
