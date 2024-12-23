import os
import json
import pandas as pd

from multi_time_series_connectedness import Volatility, Connectedness
from model.market_price_movement_prediction.etl import ETL

if __name__ == "__main__":
    volatility = Volatility(n=2)
    with open("model_config.json", "r") as file:
        config = json.load(file)
    washed_train_dir = config["washed_train_dir"]
    raw_train_dir = config["raw_train_dir"]
    train_from = config["train_from"]
    train_to = config["train_to"]
    graph_dir = config["graph_dir"]
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)

    # Process the data
    print("modifying data")
    etl = ETL(raw_train_dir, washed_train_dir)
    etl.load_data()
    etl.transform_into_same_timestamp(train_from, train_to)

    volatility.calculate(washed_train_dir, f"{graph_dir}/volatilities.pickle")
    volatilities = pd.read_pickle(f"{graph_dir}/volatilities.pickle")
    conn = Connectedness(volatilities.dropna(), 20, 200)
    conn.calculate()
    conn.store_graph_data()
    print(conn.full_connectedness)
    conn.flatten_connectedness()
