import pandas as pd
from sklearn.tree import DecisionTreeRegressor

def run_model(data):
    features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

    y = data.Price
    x = data[features]

    model = DecisionTreeRegressor(random_state=1)
    model.fit(x, y)
    
    return(model.predict(x.head()))