# Should deal with different timezone issue
import os
import pandas as pd
from pathlib import Path


class ETL:
    def __init__(self, raw_file_dir, washed_file_dir):
        self.raw_file_dir = Path(raw_file_dir)
        self.washed_file_dir = Path(washed_file_dir)
        self.csv_files = list(self.raw_file_dir.glob("*.csv"))
        self.dict_data = None

    def load_data(self):
        names = [file.stem for file in self.csv_files]
        self.dict_data = {
            name: pd.read_csv(file, index_col="time")[["Open", "High", "Low", "Close"]]
            for name, file in zip(names, self.csv_files)
        }

    def transform_into_same_timestamp(self, timestamp_from=None, timestamp_to=None):
        if not os.path.exists(self.washed_file_dir):
            os.makedirs(self.washed_file_dir)
        for name, df in self.dict_data.items():
            if timestamp_from is None:
                df.index[0]
            if timestamp_to is None:
                df.index[-1]
            washed_df = df.reindex(
                list(range(timestamp_from, timestamp_to + 1, 60))
            ).fillna(method="ffill")
            washed_df.to_csv(f"{self.washed_file_dir}/{name}.csv")

    def check_same_time_span(self):
        files = os.listdir(self.raw_file_dir)
        csv_files = [file for file in files if file.endswith(".csv")]
        data = pd.read_csv(os.path.join(self.raw_file_dir, csv_files[0]))
        first_time_sapn = [data.iloc[0]["time"], data.iloc[-1]["time"]]
        for csv_file in csv_files:
            data = pd.read_csv(os.path.join(self.raw_file_dir, csv_file))
            if [data.iloc[0]["time"], data.iloc[-1]["time"]] != first_time_sapn:
                print(f"Time span of {csv_file} is different from others")
                return False
        print(f"All time spans are the same, {first_time_sapn}")
        return True
