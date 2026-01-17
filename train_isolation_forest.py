import pandas as pd
from sklearn.ensemble import IsolationForest

print("Loading data...")
df = pd.read_csv("game_admin_derived.csv")
features = ['hour_of_day', 'actions_per_min', 'is_rare_ip']
X = df[features]
print(f"Training on {len(df)} logs with features: {features}")

# contamination=0.02 means "I guess about 2% of my data is bad."
# (We injected 200 hacks into ~15,000 logs, so ~1-2% is a good guess)
model = IsolationForest(contamination=0.02, random_state=42)
print("Training the model...")
model.fit(X)
df['anomaly_score'] = model.predict(X) #1 = Normal and -1 = Rogue
print("\n--- RESULTS ---")
hacks = df[df['anomaly_score'] == -1]
print(f"Total Anomalies Found: {len(hacks)}")
df.to_csv("game_admin_results.csv", index=False)
print("\nResults saved to 'game_admin_results.csv'. Check it out.")
hacks.to_csv("suspected_culprits3.csv", index=False)
print("\nSuspects saved to 'suspected_culprits.csv'. Check it out.")