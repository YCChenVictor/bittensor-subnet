# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import numpy as np
from typing import List, Dict, Union
import bittensor as bt
import yfinance as yf
from model.market_price_movement_prediction.scrape_finance_data_yahoo import get_historical_price_with_yfinace


def smape(real, predicted):
    return np.mean(np.abs(real - predicted) / ((np.abs(real) + np.abs(predicted)) / 2)) * 100


def reward(timestamp: int, response: Dict[str, Union[float, str]]) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """
    # The response: {'movement_prediction': 0.00011253909906372428, 'target_symbol': 'AUDCAD=X'}
    # The reward calculated by MSE
    movement_prediction = response['movement_prediction']
    symbol = response['target_symbol']
    historical_price_data = get_historical_price_with_yfinace(symbol)
    result = next((item for item in historical_price_data if item['time'] == timestamp), None)
    movement = result['Close'] - result['Open']
    reward = smape(movement, movement_prediction)

    bt.logging.info(
        f"In rewards, timestamp val: {timestamp}, response val: {response}, reward val: {reward}"
    )
    return reward


def get_rewards(
    self,
    timestamp: int,
    responses: List[Dict[str, Union[float, str]]],
) -> np.ndarray:
    """
    Returns an array of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[float]): A list of responses from the miner.

    Returns:
    - np.ndarray: An array of rewards for the given query and responses.
    """

    return np.array([reward(timestamp, response) for response in responses])
