from datetime import datetime
import time

# Original datetime string
datetime_str = "2024-10-18T07:06:00+01:00"

# Parse the datetime string
dt = datetime.fromisoformat(datetime_str)

# Convert to Unix timestamp
timestamp = int(time.mktime(dt.timetuple()))

print(timestamp)
