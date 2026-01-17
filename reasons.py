import pandas as pd

print("Loading results...")
df = pd.read_csv("suspected_culprits.csv")
suspects = df[df['anomaly_score'] == -1].copy()

def explain_flag(row):
    reasons = []
    if row['actions_per_min'] > 5:
        reasons.append("High Speed")
    if row['is_rare_ip'] == 1:
        reasons.append("Unknown IP")
    if row['hour_of_day'] < 6:  # Before 6 AM
        reasons.append("Unusual Time")
    return " + ".join(reasons)

suspects['reason'] = suspects.apply(explain_flag, axis=1)
report_columns = [
    'timestamp', 'admin_id', 'action',
    'ip_address', 'actions_per_min', 'reason'
]
final_report = suspects[report_columns]
final_report.to_csv("suspected_culprits_reasoned.csv", index=False)
print(f"--- REPORT GENERATED ---")
print(f"Found {len(final_report)} suspicious activities.")
print("Saved to 'suspected_culprits_reasoned.csv'")
print(final_report.head())