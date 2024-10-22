import os
import pandas as pd
import json
from multi_time_series_connectedness import (
    Volatility,
    RollingConnectedness,
)
from model.market_price_movement_prediction.movement import Movement
from model.market_price_movement_prediction.model_trainer import ModelTrainer

with open('model_config.json', 'r') as file:
    config = json.load(file)
raw_train_dir = config['raw_train_dir']
washed_train_dir = config['washed_train_dir']
train_dir = config['train_dir']
if not os.path.exists(washed_train_dir):
    os.makedirs(washed_train_dir)
if not os.path.exists(train_dir):
    os.makedirs(train_dir)
volatilities_filename = f"{train_dir}/volatilities.pickle"
roll_conn_filename = f"{train_dir}/roll_conn.pickle"
movement_filename = f"{train_dir}/movement.pickle"
max_lag = 20
# train_from >= volatilities_from + periods_per_volatility
periods_per_volatility = config['periods_per_volatility']
predict_symbol = config['predict_symbol']
past_roll_conn_period = config['past_roll_conn_period']

print("calculating volatilities")
volatility = Volatility(n=2)
volatility.calculate(
    washed_train_dir,
    volatilities_filename,
)

# Should enable choosing the tickers
print("calculate rolling connectedness")
volatilities = pd.read_pickle(volatilities_filename)
roll_conn = RollingConnectedness(
    volatilities.dropna(),
    max_lag,
    periods_per_volatility,
)
roll_conn.calculate(roll_conn_filename)

print("calculate movements")
movement = Movement(
    f"{washed_train_dir}/{predict_symbol}.csv", movement_filename
)
movement.get_movements("value")
movement.store()

print("train LSTM model")
with open(movement_filename, "rb") as f:
    movement = pd.read_pickle(f)
with open(roll_conn_filename, "rb") as f:
    roll_conn = pd.read_pickle(f)
model_trainer = ModelTrainer(movement, roll_conn, past_roll_conn_period, raw_train_dir, "trained_model.keras")
model_trainer.match()
model_trainer.train()
