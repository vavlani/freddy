import requests
import os
import logging
import pandas as pd
from datetime import datetime
import time
from config import FRED_API_KEY
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_all_categories(api_key, max_depth=1):
    """
    Fetches all categories from the FRED API.

    Parameters:
    api_key (str): Your FRED API key.

    Returns:
    list: A list of dictionaries containing category IDs and names.
    """
    base_url = 'https://api.stlouisfed.org/fred/category/children'
    params = {
        'api_key': api_key,
        'file_type': 'json'
    }
    
    def fetch_child_categories(category_id, parent_name, current_depth):
        params['category_id'] = category_id
        logging.info(f"Making API request to {base_url} with params: {params}")
        response = requests.get(base_url, params=params)
        logging.info(f"Received response with status code: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()
        categories = data['categories']
        for category in categories:
            category['parent_id'] = category_id
            category['parent_name'] = parent_name
            category['level'] = current_depth
        return categories
    
    all_categories = []
    categories_to_fetch = [(0, "Root", 1)]  # Start with the parent category ID 0, name "Root", and level 1
    
    while categories_to_fetch:
        current_category_id, parent_name, current_depth = categories_to_fetch.pop()
        if current_depth > max_depth:
            continue
        child_categories = fetch_child_categories(current_category_id, parent_name, current_depth)
        all_categories.extend(child_categories)
        categories_to_fetch.extend([(cat['id'], cat['name'], current_depth + 1) for cat in child_categories])
        
        # Rate limiting: sleep for 0.6 seconds to ensure we don't exceed 100 requests per minute
        time.sleep(0.6)
    
    logging.info(f"Fetched {len(all_categories)} categories from the API")
    
    return all_categories

if __name__ == "__main__":
    logging.info("Starting category fetch script")
    parser = argparse.ArgumentParser(description="Fetch all categories from FRED.")
    parser.add_argument("--max_depth", type=int, default=1, help="The maximum depth to fetch categories. Default is 1.")
    args = parser.parse_args()

    categories = fetch_all_categories(api_key=FRED_API_KEY, max_depth=args.max_depth)

    # Create the data/categories folder if it doesn't exist
    categories_folder = os.path.join("data", "categories")
    logging.info(f"Saving categories to folder: {categories_folder}")
    if not os.path.exists(categories_folder):
        os.makedirs(categories_folder)

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(categories_folder, f"categories_{timestamp}.json")

    # Convert the categories to a DataFrame and save it as a CSV file
    df = pd.json_normalize(categories)
    csv_file_path = os.path.join(categories_folder, f"categories_{timestamp}.csv")
    df.to_csv(csv_file_path, index=False)

    logging.info(f"Categories saved to {csv_file_path}")
