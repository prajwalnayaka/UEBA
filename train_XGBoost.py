import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

ds = pd.read_csv("game_admin_derived.csv")

# 1. Prepare Data
X =  ds[["hour_of_day", "actions_per_min", "is_rare_ip"]]
y = ds['is_attack']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Initialize XGBoost
# scale_pos_weight calculation: sum(negative) / sum(positive)
# This tells the model: "Pay X times more attention to the Attacks because they are rare."
ratio = float(np.sum(y == 0)) / np.sum(y == 1)

model = xgb.XGBClassifier(
    objective='binary:logistic',
    scale_pos_weight=ratio,
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)

# 3. Train
print("Training XGBoost...")
model.fit(X_train, y_train)

# 4. Predict
y_pred = model.predict(X_test)

# 5. Evaluate
print("\n--- XGBoost Performance ---")
print(classification_report(y_test, y_pred))