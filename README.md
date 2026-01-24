
# UEBA
___

UEBA stands for User & Entity Behavior Analysis. Its the process of identifying a baseline normal behabvior, training a machine learning model to learn the characteristics of the normal behabvior and using it to idetify and isolate outliers.


In light of the security failure of Rainbow 6:Seige of Ubisoft in late December of 2025, I created a very rudimentary and barebones dataset of "game admins". Since real admin logs are sensitive/private, I created a synthetic dataset using Python's Faker and NumPy. It has 5 admin entities, whose actions are logged over a period of 30 days.

I injected some "suspicious" behabvior into the logs. Extracted features from this generated dataset, implemented unsupervised learning to identify the suspect via an isolation forest. I utilized unsupervised learning because the attack pattrens constanlty evolve and change in cybersecuirty. Created a simple dashboard visualizing the results.


### data_synthesis.py
___

This script creates a dataset of logs. It comprises of timestamp, admin_id, action performed, admin's IP address and status of action. Poisson distribution is used to detemine the number of actions an admin performs per day, this is done to best simulate how people naturally work.

### feature_engineering.py
___

Here I extract features from the generated dataset that can be used to detemine whether an admin has gone rogue or is working normally. These feature are: hour of the day the action is peformed, number of actions performed per second and if the IP address of the admin is different from the one they mostly use.

### train_isolation.py
___

I chose to train an isolation forest given the low complexity of the dataset. I set the contamination value to 00.2 to align with the known prevalence of insider threats in the synthetic dataset.

### dashboard.py
___

I used streamlit and altair to create and present a simple dashboard which would be used in Security Operation Center(SOC). 


## Run it locally
___

If you want this project on your local machine:


# 1. Clone the repository
```
git clone https://github.com/prajwalanayakat/UEBA.git
```
# 2. Navigate to the project directory
```
cd UEBA
```
# 3. Install dependencies
```
pip install -r requirements.txt
```
# 4. Run the dashboard
```
streamlit run dashboard.py
```
