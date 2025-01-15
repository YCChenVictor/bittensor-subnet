import json

with open("model_config.json", "r") as file:
    model_config = json.load(file)

train_symbols = model_config["train_symbols"]
self_connectedness_columns = list(map(lambda symbol: symbol + ".csv" + "_to_" + symbol + ".csv", train_symbols))
columns_to_remove = [
    "end_at",
    "start_at",
    "forecast_period",
] + self_connectedness_columns
