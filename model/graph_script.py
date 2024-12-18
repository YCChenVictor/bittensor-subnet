import os
import json
import pandas as pd

from multi_time_series_connectedness import Volatility, Connectedness

if __name__ == "__main__":
    volatility = Volatility(n=2)
    with open("model_config.json", "r") as file:
        data = json.load(file)
    washed_train_dir = data["washed_train_dir"]
    graph_dir = data["graph_dir"]
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    volatility.calculate(washed_train_dir, f"{graph_dir}/volatilities.pickle")
    volatilities = pd.read_pickle(f"{graph_dir}/volatilities.pickle")
    conn = Connectedness(volatilities.dropna(), 10)
    conn.calculate()
    conn.store_graph_data()
    conn.flatten_connectedness()
