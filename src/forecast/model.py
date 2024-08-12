import pandas as pd
from sklearn.tree import DecisionTreeRegressor

def run_model(data):
    # melbourne_file_path = 'sample_data/melb_data.csv'

    #data = pd.read_csv(melbourne_file_path) 
    data = data.dropna(axis=0)

    features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

    y = data.Price
    x = data[features]

    # print(x.head())

    model = DecisionTreeRegressor(random_state=1)
    model.fit(x, y)

    print("Predictions on following 5 houses: ")
    print(x.head())
    print("Predictions are: ")
    print(model.predict(x.head()))