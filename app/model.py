import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib


data = pd.read_csv("data/aqi_data.csv")


X = data[['temperature','humidity','wind_speed','traffic_level']]
y = data['aqi']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = RandomForestRegressor()
model.fit(X_train, y_train)


joblib.dump(model, "models/aqi_model.pkl")

print("Model trained and saved!")