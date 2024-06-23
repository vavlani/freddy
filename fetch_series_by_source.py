import os
import time
import requests
import pandas as pd
import logging
from config import FRED_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_series_by_source(tag_source_name, limit=50):
    """
    Fetch series for a given source from the FRED API and store them in separate CSV files.
    
    Parameters:
    tag_source_name (str): The name of the source.
    limit (int): The maximum number of series to fetch.
    """
    logging.info(f"Starting to fetch series for source: {tag_source_name}")
    url = f"https://api.stlouisfed.org/fred/series/search?tag={tag_source_name}&api_key={FRED_API_KEY}&file_type=json&limit={limit}"
    logging.info(f"Requesting URL: {url}")
    response = requests.get(url)
    logging.info(f"Received response with status code: {response.status_code}")
    data = response.json()
    series_list = data.get('seriess', [])

    offset = 0
    
    source_folder = os.path.join('data', 'series', 'source', tag_source_name)
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)
    
    logging.info(f"Total series fetched: {len(series_list)}")
    for i, series in enumerate(series_list):
        logging.info(f"Processing series {i+1}/{len(series_list)}: {series['id']}")
        series_id = series['id']
        series_file_path = os.path.join(source_folder, f"{i+1}.csv")
        df = pd.DataFrame([series])
        df.to_csv(series_file_path, index=False)
        logging.info(f"Saved series {series_id} to {series_file_path}")
        time.sleep(0.5)  # Sleep to avoid hitting API rate limits

def main():
    tags_file_path = os.path.join('data', 'source_tags', 'source_tags.csv')
    source_tags_df = pd.read_csv(tags_file_path)
    source_tags_df = source_tags_df.loc[source_tags_df['name'] == 'irs']
    
    for _, row in source_tags_df.iterrows():
        source_name = row['name']
        fetch_series_by_source(source_name)

if __name__ == '__main__':
    main()
