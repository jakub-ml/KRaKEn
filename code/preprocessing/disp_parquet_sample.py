import pandas as pd
import numpy as np
from config import MERGED_DATA_PATH
import os

# load S01_data.parquet
df = pd.read_parquet(os.path.join(MERGED_DATA_PATH, 'all_users_data.parquet'))

s01 = df[df['user_id'] == 'S01']
df[df['user_id'] == 'S01'] = np.nan
# drop nan in user_id
df = df.dropna(subset=['user_id'])

# sample 10000 rows from s01
s01_sample = s01.sample(n=10000, random_state=44)

df = pd.concat([s01_sample, df], ignore_index=True)

df.to_parquet(os.path.join(MERGED_DATA_PATH, "fixed.parquet"))