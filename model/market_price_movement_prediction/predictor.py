import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import asyncio
from multi_time_series_connectedness import Volatility, RollingConnectedness
from model.market_price_movement_prediction.scrape_finance_data_yahoo import (
    scrape_and_save_data,
)
from model.market_price_movement_prediction.data_utils import columns_to_remove
from model.market_price_movement_prediction.etl import ETL


class Predictor:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        with open("model_config.json", "r") as file:
            self.model_config = json.load(file)

    def predict(self, timestamp: int):
        print("scraping finance data for predicting")
        asyncio.run(
            scrape_and_save_data(
                self.model_config["train_symbols"],
                self.model_config["raw_predict_dir"],
            )
        )

        print("modifying data")
        past_roll_conn_period = self.model_config["past_roll_conn_period"]
        periods_per_volatility = self.model_config["periods_per_volatility"]
        volatilities_from = (
            timestamp - (past_roll_conn_period + periods_per_volatility + 1) * 60
        )
        volatilities_to = timestamp
        etl = ETL(
            self.model_config["raw_predict_dir"],
            self.model_config["washed_predict_dir"],
        )
        etl.load_data()
        etl.transform_into_same_timestamp(volatilities_from, volatilities_to)

        print("calculating volatilities")
        volatility = Volatility(n=2)
        predict_dir = self.model_config["predict_dir"]
        if not os.path.exists(predict_dir):
            os.makedirs(predict_dir)
        volatility.calculate(
            self.model_config["washed_predict_dir"],
            f"{predict_dir}/volatilities.pickle",
        )

        print("calculate rolling connectedness")
        volatilities = pd.read_pickle(f"{predict_dir}/volatilities.pickle")
        roll_conn = RollingConnectedness(
            volatilities.dropna(),
            self.model_config["max_lag"],
            periods_per_volatility,
        )
        roll_conn.calculate()
        roll_conn.store(f"{predict_dir}/roll_conn.pickle")

        print("predict movements")
        with open(f"{predict_dir}/roll_conn.pickle", "rb") as f:
            predict_roll_conn = pd.read_pickle(f)
        predict_roll_conn.set_index("forecast_at", inplace=True)
        input_data = predict_roll_conn.drop(columns=columns_to_remove).values
        input_data = np.expand_dims(input_data, axis=0)
        prediction = self.model.predict(input_data)
        return prediction
