import os
import json
import requests
import logging
import pandas as pd
from config import FRED_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_all_sources():
    """
    Fetch all sources of economic data from the FRED API.
    """
    logging.info("Fetching all sources of economic data from the FRED API")
    url = f"https://api.stlouisfed.org/fred/sources?api_key={FRED_API_KEY}&file_type=json"
    logging.info(f"Requesting URL: {url}")
    response = requests.get(url)
    logging.info(f"Received response with status code: {response.status_code}")
    data = response.json()
    sources = data['sources']
    
    sources_folder = 'data/sources'
    if not os.path.exists(sources_folder):
        os.makedirs(sources_folder)
    
    sources_file_path = os.path.join(sources_folder, 'sources.csv')
    df = pd.DataFrame(sources)
    df.to_csv(sources_file_path, index=False)
    logging.info(f"Saved all sources to {sources_file_path}")
    
    logging.info(f"All sources have been saved to {sources_file_path}")

if __name__ == '__main__':
    fetch_all_sources()
