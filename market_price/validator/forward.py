# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import datetime
import bittensor as bt

from market_price.protocol import MarketPriceSynapse
from market_price.validator.reward import get_rewards
from market_price.utils.uids import get_random_uids


async def forward(self):
    """
    The forward function is called by the validator every time step.

    It is responsible for querying the network and scoring the responses.

    Args:
        self (:obj:`bittensor.neuron.Neuron`): The neuron object which contains all the
        necessary state for the validator.
    """
    # Wait for the start of the next minute. (Maybe next minute + 1 second)
    now = datetime.datetime.now()
    wait_time = 60 + 5 - now.second - now.microsecond / 1_000_000
    time.sleep(wait_time)

    # It should get miner uids
    # However it actually get all the uids, including non miner uids
    # The non miner uids should be blacklisted by the blackedlist mechanism
    uids = get_random_uids(
        self, k=min(self.config.neuron.sample_size, self.metagraph.n.item())
    )

    target_timestamp = int(time.time()) - 5
    # The dendrite client queries the network.
    responses = await self.dendrite(
        # Send the query to selected miner axons in the network.
        axons=[self.metagraph.axons[uid] for uid in uids],
        synapse=MarketPriceSynapse(timestamp=target_timestamp),
        # All responses have the deserialize function called on them before returning.
        # You are encouraged to define your own deserialization function.
        deserialize=True,
    )

    # Log the results for monitoring purposes.
    bt.logging.info(f"Received responses: {responses}")

    # Adjust the scores based on responses from miners.
    rewards = get_rewards(self, timestamp=target_timestamp, responses=responses)

    # Still did not resolve the non miner issue, the forward will request result on all
    # uids in the current neuron

    bt.logging.info(f"Scored responses: {rewards}")
    # Let's just trust the update scores mechanism
    self.update_scores(rewards, uids)
