import xgboost as xgb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

ds = pd.read_csv("game_admin_derived.csv")

# 1. Prepare Data
X = ds[["hour_of_day", "actions_per_min", "is_rare_ip"]]
y = ds["is_attack"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
classes = ['Normal','Malicious']

# 2. Initialize XGBoost
model = xgb.XGBClassifier(
    objective="binary:logistic",
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss",
)

# 3. Train
print("Training XGBoost...")
evalset = [(X_train, y_train), (X_test, y_test)]

model.fit(
    X_train, y_train,
    eval_set=evalset,
    verbose=False
)

# 4. Predict
y_pred = model.predict(X_test)

# 5. Evaluate
print("\n--- XGBoost Performance ---")
print(classification_report(y_test, y_pred,target_names=['Normal','Rogue']))
results = model.evals_result()
train_loss = results['validation_0']['logloss']
test_loss = results['validation_1']['logloss']

plt.figure(figsize=(8, 5))
plt.plot(train_loss, label='Training Loss', color='green')
plt.plot(test_loss, label='Testing Loss', color='red', linestyle='--')

plt.title('XGBoost: Training vs Testing Loss')
plt.xlabel('Number of Trees (Estimators)')
plt.ylabel('Log Loss (Lower is Better)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('XGB_Train_vs_Test.png',dpi=600)
plt.show()

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True, fmt="d",cmap="YlGnBu",xticklabels=classes, yticklabels=classes)
plt.savefig('XGBoost_Confusion_Matrix.png',dpi=600)
plt.title('Confusion Matrix')
plt.show()