import asyncio
import json
from model.market_price_movement_prediction.scrape_finance_data_yahoo import (
    scrape_and_save_data,
)

with open("model_config.json", "r") as file:
    config = json.load(file)
train_dir = config["train_dir"]
tickers = config["train_symbols"]
raw_train_dir = config["raw_train_dir"]
washed_train_dir = config["washed_train_dir"]
train_from = config["train_from"]
train_to = config["train_to"]

# scrape data from training
print("scraping finance data for training")
asyncio.run(scrape_and_save_data(tickers, raw_train_dir))
