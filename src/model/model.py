import pandas as pd
import numpy as np

import joblib

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from pathlib import Path

# https://www.kaggle.com/code/dansbecker/your-first-machine-learning-model
# sample_data/melb_data.csv
# sample_data/melb_data_np.csv

base_path = Path(__file__).parent
modelpkldump_path = Path(__file__).parent.parent.parent

csv_file = base_path / "sample_data" / "melb_data.csv"
data = pd.read_csv(csv_file)
data.columns
data.describe()

features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

y = data['Price']

print(" ")
print("--- Y Data")
print(y.values)
print(" ")

X = data[features]

print(" ")
print("--- X Data")
print(X.values)
print(" ")

# Price is NaN in some rows so we will need to fill in the data
# ....
#   File "/forecast/src/model/model.py", line 29, in <module>
#   model.fit(train_X, train_y)
# ....
#   ValueError: Input y contains NaN.

y = y.fillna(y.median())

# https://www.kaggle.com/code/dansbecker/model-validation
train_X, val_X, train_y, val_y = train_test_split(X.values, y.values, test_size=0.2, random_state = 1)

model = DecisionTreeRegressor(random_state=1)
model.fit(train_X, train_y)

# get predicted prices on validation data
# val_predictions = melbourne_model.predict(val_X)
# print(mean_absolute_error(val_y, val_predictions))

# testing the model
#arr = np.array([8.3252, 41.0, 6.984127, 1.02381, 322.0]).reshape(1, -1)
#print(model.predict(arr.reshape(1, -1)))

# 'data/model.pkl'
modelpkldump_file = modelpkldump_path / "data" / "forecastmodel.pkl"

# save the model 
joblib.dump(model, modelpkldump_file)

