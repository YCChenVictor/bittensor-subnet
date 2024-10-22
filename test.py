import time
import datetime

now = datetime.datetime.now()
wait_time = wait_time = 65 - now.second - now.microsecond / 1_000_000
time.sleep(wait_time)
timestamp = int(time.time())
print(timestamp)
