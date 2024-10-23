responses = [1, -999]
uids = [0, 1]

miner_responses = [response for response in responses if response >= 0]
miner_uids = [uids[i] for i, response in enumerate(responses) if response >= 0]

print(miner_responses)
print(miner_uids)
