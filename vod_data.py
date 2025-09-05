import pandas
from datetime import datetime,timedelta
import random

import pandas as pd

platforms = ["NOW TV","SKY Q","SKY GLASS","SKY GO"]
checks = ["NO_WATCH_ONLINE_OPTION","NO_WATCH_ONLINE_OPTION_IN_SEARCH","OFFER_NOT_AVAILABLE_VIA_WAYS_TO_WATCH_SEARCH"]
status = ["Awaiting Fix","No Fault Found","Self Resolved"]

def generate_dummy_data(num_rows=5000):
    data = []
    base_date = datetime.now()

    for _ in range(num_rows):
        first_seen = base_date -timedelta(days = random.randint(0,30),hours=random.randint(0,23),minutes=random.randint(0,59))
        duration = timedelta(hours=random.randint(0,4),minutes=random.randint(0,59))
        last_seen = first_seen - duration
        row = {
            "timestamp": (base_date - timedelta(days=random.randint(0,30))).strftime("%Y-%m-%d"),
            "platform": random.choice(platforms),
            "check": random.choice(checks),
            "status": random.choices(status, weights=[0.3,0.5,0.2])[0],
            "first_seen": first_seen,
            "last_seen": last_seen
        }
        data.append(row)
    return pd.DataFrame(data)

df = generate_dummy_data()
