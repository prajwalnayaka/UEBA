from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ds = pd.read_csv("game_admin_derived.csv")
X = ds[["hour_of_day", "actions_per_min", "is_rare_ip"]]
y = ds["is_attack"]
class_names=['Normal','Malicious']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("\n--- Logistic Regression Performance ---")
print(classification_report(y_test, y_pred,target_names=['Normal','Rogue']))
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True,fmt="d",cmap="YlGnBu",xticklabels=class_names,yticklabels=class_names)
plt.savefig("Performance/LR_Confusion_Matrix.png",dpi=600)
plt.show()
