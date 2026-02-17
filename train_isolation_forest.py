import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

ds = pd.read_csv("game_admin_derived.csv")
features = ["hour_of_day", "actions_per_min", "is_rare_ip"]
X = ds[features]
model = IsolationForest(contamination="auto", random_state=1)
model.fit(X)
preds = model.predict(X)

# If pred is -1 (anomaly), we call it 1 (attack). Otherwise, 0.
ds["pred_label"] = [1 if x == -1 else 0 for x in preds]
# scores = model.decision_function(X)
# plt.figure(figsize=(10, 8))
# plt.plot(np.sort(scores))
# plt.xlabel("Data Points")
# plt.ylabel("Anomaly Score (Lower is worse)")
# plt.grid(True)
# plt.show()

print("\n--- Isolation Forest Performance ---")
y_true = ds["is_attack"]
y_pred = ds["pred_label"]

print(classification_report(y_true, y_pred, target_names=["Normal", "Rogue"]))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(f"True Negatives (Normal detected as Normal): {cm[0][0]}")
print(f"False Positives (Normal flagged as Attack): {cm[0][1]}")
print(f"False Negatives (Attack missed): {cm[1][0]}")
print(f"True Positives (Attack caught): {cm[1][1]}")

# Save results as before
ds["anomaly_score"] = preds
ds.to_csv("game_admin_results.csv", index=False)
