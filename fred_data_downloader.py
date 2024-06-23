import pandas as pd
import requests
import os
import json
import logging
from config import FRED_API_KEY

SERIES_INFO_FOLDER = 'data/series_info'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_series_info(series_id):
    """
    Fetch metadata for a given series ID from the FRED API.
    """
    series_info_path = os.path.join(SERIES_INFO_FOLDER, f"{series_id}.json")
    
    if os.path.exists(series_info_path):
        logging.info(f"Loading metadata for series_id: {series_id} from local file: {series_info_path}")
        with open(series_info_path, 'r') as file:
            series_info = json.load(file)
    else:
        url = f"https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        url = f"https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        logging.info(f"Fetching metadata for series_id: {series_id} from FRED API: {url}")
        url = f"https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        response = requests.get(url)
        data = response.json()
        series_info = data['seriess'][0]
        
        if not os.path.exists(SERIES_INFO_FOLDER):
            os.makedirs(SERIES_INFO_FOLDER)
        
        with open(series_info_path, 'w') as file:
            json.dump(series_info, file)
    
    return series_info

def fetch_series_tags(series_id):
    """
    Fetch tags for a given series ID from the FRED API.
    """
    tags_folder = 'data/series_tags'
    tags_file_path = os.path.join(tags_folder, f"{series_id}.json")
    
    if os.path.exists(tags_file_path):
        logging.info(f"Loading tags for series_id: {series_id} from local file: {tags_file_path}")
        with open(tags_file_path, 'r') as file:
            tags = json.load(file)
    else:
        url = f"https://api.stlouisfed.org/fred/series/tags?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        url = f"https://api.stlouisfed.org/fred/series/tags?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        logging.info(f"Fetching tags for series_id: {series_id} from FRED API: {url}")
        url = f"https://api.stlouisfed.org/fred/series/tags?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        response = requests.get(url)
        tags = response.json()
        
        if not os.path.exists(tags_folder):
            os.makedirs(tags_folder)
        
        with open(tags_file_path, 'w') as file:
            json.dump(tags, file)
    
    return tags


def fetch_fred_data(series_id, start_date, end_date, series_info):
    """
    Fetch data from the FRED API for a given series ID and date range.
    """
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    logging.info(f"Fetching data for series_id: {series_id} from {start_date} to {end_date} using URL: {url}")
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&observation_start={start_date}&observation_end={end_date}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['observations'])
    
    # Add series info as additional columns
    for key, value in series_info.items():
        df[key] = value
    
    return df



def save_data_to_csv(df, series_id, data_folder='data'):
    """
    Save the DataFrame to a CSV file in the specified data folder.
    
    Parameters:
    df (pd.DataFrame): DataFrame to save.
    series_id (str): Series ID for naming the file.
    data_folder (str): Folder to save the CSV file in.
    """
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    file_path = os.path.join(data_folder, f"{series_id}.csv")
    logging.info(f"Saving data to file: {file_path}")
    df.to_csv(file_path, index=False)

def load_config(config_file='./data_config.json'):
    """
    Load the configuration from a JSON file.
    """
    logging.info(f"Loading configuration from file: {config_file}")
    with open(config_file, 'r') as file:
        return json.load(file)

def download_all_data(config_file='data_config.json'):
    """
    Download all data specified in the configuration file.
    """
    config = load_config(config_file)
    logging.debug(config)
    for series in config['series']:
        series_id = series['series_id']
        logging.info(f"Checking and processing series: {series_id}")
        
        # Fetch series metadata
        series_info = fetch_series_info(series_id)
        logging.info(f"Series Info: Title: {series_info['title']}, Frequency: {series_info['frequency']}, Units: {series_info['units']}, Seasonal Adjustment: {series_info['seasonal_adjustment']}, Last Updated: {series_info['last_updated']}")
        series_id = series['series_id']
        start_date = series['start_date']
        end_date = series['end_date']
        df = fetch_fred_data(series_id, start_date, end_date)
        save_data_to_csv(df, series_id, data_folder='data')
    logging.info("All data downloaded successfully.")

if __name__ == '__main__':
    download_all_data(config_file='data_config.json')
