import unittest
from unittest.mock import patch
import pandas as pd
from pathlib import Path

from model.market_price_movement_prediction.etl import ETL


class TemplateValidatorNeuronTestCase(unittest.TestCase):
    def setUp(self):
        # Mock the return value of Path.glob to simulate CSV files
        self.patcher_glob = patch('pathlib.Path.glob', return_value=[Path('file1.csv'), Path('file2.csv')])
        self.mock_glob = self.patcher_glob.start()

        # Mock the return value of pandas.read_csv to simulate reading CSV files
        self.patcher_read_csv = patch('pandas.read_csv', return_value=pd.DataFrame({
            'time': [1730678400, 1730678460, 1730678520, 1730678580, 1730678640],
            'Open': [1, 2, 3, 4, 5],
            'High': [2, 3, 4, 5, 6],
            'Low': [0, 1, 2, 3, 4],
            'Close': [1.5, 2.5, 3.5, 4.5, 5.5]
        }).set_index('time'))
        self.mock_read_csv = self.patcher_read_csv.start()

        # Initialize the ETL instance
        self.etl = ETL("tests/data", "tests/washed_data")

    def tearDown(self):
        self.patcher_glob.stop()
        self.patcher_read_csv.stop()

    def test_load_data(self):
        self.etl.load_data()
        self.assertIsNotNone(self.etl.dict_data)
        self.assertIn('file1', self.etl.dict_data)
        self.assertIn('file2', self.etl.dict_data)
