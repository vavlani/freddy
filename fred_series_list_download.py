import requests
import pandas as pd
import config

# Replace with your FRED API key
api_key = config.FRED_API_KEY

from fredapi import Fred
fred = Fred(api_key=api_key)

categories_file = './data/sources/sources.csv'
df_cat = pd.read_csv(categories_file)

print(df_cat.shape)
