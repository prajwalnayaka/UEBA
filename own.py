import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta


f=Faker()
np.random.seed(0)
number_of_admins=5
number_of_days=30
start_date=datetime(2024,1,1)
average_actions_per_day=50
admins=[f"admin_{i}" for i in range(1, number_of_admins+1)]
IPs={admin:f.ipv4() for admin in admins}
location={admin:f.country_code() for admin in admins}

actions=["login","logout","view_profile","ban","unban","moderate_currency","reset_password"]
weights=[0.1,0.1,0.5,0.05,0.05,0.05,0.15]
data=[]

for day in range(number_of_days):
    current_date=start_date+timedelta(days=day)
    for admin in admins:
        if random.random>0.1:
            num_actions=np.random.poisson(average_actions_per_day)
            for _ in range(num_actions):
                hour=int(np.random.normal(14,2))
                minute=np.random.randint(0,60)
                second=np.random.randint(0,60)
                actions=np.random.choice(actions,p=weights)
                ip=IPs[admin] if random.random()>0.01 else f.ipv4()
                timestamp=current_date+timedelta(hours=max(0,min(23,hour)),minutes=minute,seconds=second)

                data.append({
                    'admin':admin,
                    'ip':ip,
                    'timestamp':timestamp,
                    'actions':actions,
                    'status':"Success"
                })

hacker_time=start_date+timedelta(days=7)
hacker_time.replace(hour=3,minute=0,second=0)
for i in range(200):
    data.append({
        'admin': 'admin_1',
        'ip': IPs["admin_1"],
        'timestamp': hacker_time+timedelta(days=i*3),
        'actions': 'ban',
        'status': "Success"
    })
