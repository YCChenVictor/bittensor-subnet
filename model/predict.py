import pandas as pd
import numpy as np
import json

from model.market_price_movement_prediction.predictor import Predictor

with open("model_config.json", "r") as file:
    config = json.load(file)
predict_symbol = config["predict_symbol"]
df = pd.read_csv(f'model/docs/market_prices/train/{predict_symbol}.csv')
predictor = Predictor("trained_model.keras")

result = {}
for i in range(10):
    timestamp = 1735541700 + i * 60
    print(timestamp)
    row = df[df['time'] == (timestamp)]
    real = row["Close"].values[0] - row["Open"].values[0]
    print(real)
    prediction = predictor.predict(timestamp)[0]
    print(prediction)
    result[timestamp] = {"real": real, "prediction": prediction}
print(result)
