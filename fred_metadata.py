import requests
import os
import json
from datetime import datetime
import logging
import pandas as pd
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_all_series_metadata(category_id, api_key=config.FRED_API_KEY, limit=20):
    # Define the metadata folder and file path
    metadata_folder = os.path.join("data", "metadata_series")
    if not os.path.exists(metadata_folder):
        os.makedirs(metadata_folder)
    csv_file_path = os.path.join(metadata_folder, f"{category_id}.csv")

    # Check if the file already exists
    if os.path.exists(csv_file_path):
        logging.info(f"File {csv_file_path} already exists. Loading data from file.")
        try:
            df_series_metadata = pd.read_csv(csv_file_path)
        except:
            df_series_metadata = None
    else:
        logging.info(f"File {csv_file_path} does not exist. Fetching data from API.")
        base_url = 'https://api.stlouisfed.org/fred/category/series'
        params = {
            'api_key': api_key,
            'category_id': category_id,
            'file_type': 'json',
            'order_by': 'popularity',
            'limit': limit,
            'sort_order': 'desc'
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        series_list = data['seriess']
        
        # Save the series metadata to a CSV file
        df_series_metadata = pd.json_normalize(series_list)
        df_series_metadata.to_csv(csv_file_path, index=False)
    
    return df_series_metadata


if __name__ == "__main__":
    pass
