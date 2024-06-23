import os
import requests
import logging
import pandas as pd
from config import FRED_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_source_tags():
    """
    Fetch all source tags from the FRED API and store them in the data/source_tags folder.
    """
    logging.info("Fetching all source tags from the FRED API")
    url = f"https://api.stlouisfed.org/fred/tags?api_key={FRED_API_KEY}&file_type=json&tag_group_id=src"
    logging.info(f"Requesting URL: {url}")
    response = requests.get(url)
    logging.info(f"Received response with status code: {response.status_code}")
    data = response.json()
    tags = data['tags']
    
    tags_folder = 'data/source_tags'
    if not os.path.exists(tags_folder):
        os.makedirs(tags_folder)
    
    tags_df = pd.DataFrame(tags)
    tags_file_path = os.path.join(tags_folder, 'source_tags.csv')
    tags_df.to_csv(tags_file_path, index=False)
    logging.info(f"Saved source tags to {tags_file_path}")
    
    logging.info(f"All source tags have been saved to {tags_file_path}")

if __name__ == '__main__':
    fetch_source_tags()
