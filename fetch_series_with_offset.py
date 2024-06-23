import os
import time
import requests
import pandas as pd
import logging
from config import FRED_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_series_with_offset(tag_source_name, limit=1000):
    """
    Fetch series for a given source from the FRED API using offset and store them in separate CSV files.
    
    Parameters:
    tag_source_name (str): The name of the source.
    limit (int): The maximum number of series to fetch per API call.
    """
    logging.info(f"Starting to fetch series for source: {tag_source_name}")
    offset = 0
    series_list = []
    
    while True:
        url = f"https://api.stlouisfed.org/fred/tags/series?tag_names={tag_source_name}&api_key={FRED_API_KEY}&file_type=json&limit={limit}&offset={offset}"
        logging.info(f"Requesting URL: {url}")
        response = requests.get(url)
        logging.info(f"Received response with status code: {response.status_code}")
        data = response.json()
        new_series = data.get('seriess', [])
        
        if not new_series:
            logging.info("No more series to fetch, exiting loop.")
            break
        
        series_list.extend(new_series)
        offset += limit
        # time.sleep(0.1)  # Sleep to avoid hitting API rate limits
    
    source_folder = os.path.join('data', 'series', 'source', tag_source_name)
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)
    
    logging.info(f"Total series fetched: {len(series_list)}")
    for i in range(0, len(series_list), limit):
        batch = series_list[i:i + limit]
        logging.info(f"Processing series batch {i//limit + 1}")
        series_file_path = os.path.join(source_folder, f"batch_{i//limit + 1}.csv")
        df = pd.DataFrame(batch)
        df['source_tag'] = tag_source_name
        df.to_csv(series_file_path, index=False)
        logging.info(f"Saved series batch {i//limit + 1} to {series_file_path}")

def combine_batches_to_dataframe(source_folder):
    """
    Combine all batch CSV files in the given source folder into one DataFrame and print df.head().
    
    Parameters:
    source_folder (str): The folder containing the batch CSV files.
    
    Returns:
    pd.DataFrame: Combined DataFrame.
    """
    logging.info(f"Combining batch CSV files in folder: {source_folder}")
    all_files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.endswith('.csv')]
    df_list = [pd.read_csv(file) for file in all_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    logging.info("Combined DataFrame head:")
    print(combined_df.head())
    return combined_df

def combine_all_source_csv():
    """
    Combine all individual CSV files under each source folder into one final CSV file.
    """
    source_base_folder = os.path.join('data', 'series', 'source')
    all_files = []
    
    for source_name in os.listdir(source_base_folder):
        source_folder = os.path.join(source_base_folder, source_name)
        if os.path.isdir(source_folder):
            all_files.extend([os.path.join(source_folder, f) for f in os.listdir(source_folder) if f.endswith('.csv')])
    
    if all_files:
        df_list = [pd.read_csv(file) for file in all_files]
        final_combined_df = pd.concat(df_list, ignore_index=True)
        final_combined_file_path = os.path.join(source_base_folder, "all_sources_combined.csv")
        final_combined_df.to_csv(final_combined_file_path, index=False)
        logging.info(f"All sources combined CSV saved to {final_combined_file_path}")

def main():
    tags_file_path = os.path.join('data', 'source_tags', 'source_tags.csv')
    source_tags_df = pd.read_csv(tags_file_path)
    # source_tags_df = source_tags_df.loc[source_tags_df['name'] == 'irs']
    
    # for _, row in source_tags_df.iterrows():
    #     source_name = row['name']
    #     fetch_series_with_offset(source_name)

    combine_all_source_csv()

   
if __name__ == '__main__':
    main()
