import random as rd
import pandas as pd
import numpy as np
number_of_days=7
average_number_of_customers=50
actions=['Sale','Eat_money','Item_stuck']
items={'Coke':'$1.50','Chips':'$1.00','Candy':'$1.00','Water':'$0.75'}
weights=[0.85,0.1,0.05]
sales=[]
for days in range(number_of_days):
    customers_today=np.random.poisson(average_number_of_customers)
    for i in range(customers_today):
        outcome=np.random.choice(actions,p=weights)
        item_sold = rd.choice(list(items.items()))
        if outcome=='Sale':
            sales.append({
                'Day':days+1,
                'Item':item_sold[0],
                'Price':item_sold[1],
                'Outcome':'Item sold successfully'
                })
        elif outcome=='Eat_money':
            sales.append({
                'Day': days + 1,
                'Item': item_sold[0],
                'Price': item_sold[1],
                'Outcome': 'Money was accepted and no item was sold.'
            })
        elif outcome=='Item_stuck':
            sales.append({
                'Day':days+1,
                'Item':item_sold[0],
                'Price':item_sold[1],
                'Outcome':'Item got stuck.'
                })
df = pd.DataFrame(sales)
df.to_csv('sales.csv',index=False)