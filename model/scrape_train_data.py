import asyncio
import json
from model.market_price_movement_prediction.scrape_finance_data_yahoo import (
    scrape_and_save_data,
)
from model.market_price_movement_prediction.etl import ETL

with open("model_config.json", "r") as file:
    data = json.load(file)
train_dir = data["train_dir"]
tickers = data["train_symbols"]
raw_train_dir = data["raw_train_dir"]
washed_train_dir = data["washed_train_dir"]
train_from = data["train_from"]
train_to = data["train_to"]

# scrape data from training
print("scraping finance data for training")
asyncio.run(scrape_and_save_data(tickers, raw_train_dir))

# Process the data
print("modifying data")
etl = ETL(raw_train_dir, washed_train_dir)
etl.load_data()
etl.transform_into_same_timestamp(train_from, train_to)
