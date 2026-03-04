
# UEBA
___

UEBA stands for User & Entity Behavior Analysis. Its the process of identifying a baseline normal behabvior, training a machine learning model to learn the characteristics of the normal behabvior and using it to identify and isolate outliers.


In light of the security failure of Rainbow 6:Seige of Ubisoft in late December of 2025, I created a very rudimentary and barebones dataset of "game admins". Since real admin logs are sensitive/private, I created a synthetic dataset using Python's Faker and NumPy. It has 5 admin entities, whose actions are logged over a period of 30 days.

I injected some "suspicious" behavior into the logs. Extracted features from this generated dataset, implemented unsupervised learning to identify the suspect via an isolation forest. I utilized unsupervised learning because the attack patterns constantly evolve and change in cybersecurity. Created a simple dashboard visualizing the results.


### data_synthesis.py
___

This script creates a dataset of logs. It comprises of timestamp, admin_id, action performed, admin's IP address and status of action. Poisson distribution is used to determine the number of actions an admin performs per day, this is done to best simulate how people naturally work. Accress it on [Kaggle.](https://www.kaggle.com/datasets/prajwalnayakat/ueba-insider-threat-and-attack-detection)

### feature_engineering.py
___

Here I extract features from the generated dataset that can be used to determine whether an admin has gone rogue or is working normally. These features are: hour of the day the action is performed, number of actions performed per second and if the IP address of the admin is different from the one they mostly use.

### train_isolation.py
___

I chose to train an isolation forest given the low complexity of the dataset. I set the contamination value to 0.3 which was determined by observing the 'elbow' graph. 
Precision: 0.67

### train_logistic_regression.py
___

Trained the logistic regression model, it works really good given the simple nature of the dataset.
Precison: 0.91

### train_XGBoost.py
___

Trained the XGBoost model, it used to overfit very easily on the primitive versions of the dataset. Used this model's metrics as a sort of quality rating on the dataset. After multiple modifictions and iterations the final datset was conceived.
Precision: 0.95

### comparison.py
___

I used streamlit and altair to create and present a simple dashboard to draw comparison between the models' performances. 


## Run it locally
___

If you want this project on your local machine:


### 1. Clone the repository
```
git clone https://github.com/prajwalanayakat/UEBA.git
```
### 2. Navigate to the project directory
```
cd UEBA
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Run the feature_engineering.py file
```
python feature_engineering.py
```
### 5. Train the models
```
python train_isolation_forest.py
python train_logistic_regression.py
python train_XGBoost.py

```
### 6. Run the dashboard
```
streamlit run comparison.py
```
---
## Streamlit Dashboard

<img width="1778" height="777" alt="1" src="https://github.com/user-attachments/assets/39ed04fc-5f6c-4ab1-8346-043b7202baf7" />

<img width="1823" height="836" alt="2" src="https://github.com/user-attachments/assets/36f9eb4c-04bd-4573-86f2-e74b5affce61" />

<img width="1772" height="732" alt="3" src="https://github.com/user-attachments/assets/5b98dbd7-f9f6-4a15-8020-9403955af56a" />

<img width="903" height="552" alt="4" src="https://github.com/user-attachments/assets/8384cc63-7110-4a08-a42b-a1ed8bd1a936" />
