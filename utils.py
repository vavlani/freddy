import pandas as pd
import logging
from openai import OpenAI
import config

def load_data(file_path):
    """
    Loads data from a CSV file.
    
    Parameters:
    file_path (str): Path to the CSV file.
    
    Returns:
    pd.DataFrame: DataFrame containing the loaded data.
    """
    logging.info(f"Loading data from file: {file_path}")
    return pd.read_csv(file_path)

def load_category_data(data_file):
    df = pd.read_csv(data_file)
    df = df.fillna('')
    df['notes'] = df['notes'].str.wrap(50).apply(lambda x: x.replace('\n', '<br>'))
    df = df.fillna('')
    df['id'] = df['id'].astype(str)
    df['parent_id'] = df['parent_id'].astype(str)
    df['parent_id'] = df['parent_id'].replace('0', 'All categories')
    df['count'] = 1

    unique_ids = set(df['id'])
    df['parent_id'] = df['parent_id'].apply(lambda x: x if x in unique_ids or x == 'All categories' else 'All categories')

    logging.info(f"Loaded category data from file: {data_file}")
    return df

def call_openai(user_prompt, model_name='gpt-4o', system_prompt=None, max_tokens=500):
    """
    Function to call OpenAI API and get a response.

    Parameters:
    model_name (str): The name of the OpenAI model to use.
    user_prompt (str): The prompt to send to the model.
    system_prompt (str): An optional system prompt to provide context.
    max_tokens (int): The maximum number of tokens to generate.

    Returns:
    str: The response from the OpenAI model.
    """
    logging.info("Initializing OpenAI client")
    client = OpenAI(
        api_key=config.OPENAI_API_KEY,
    )
    
    logging.info("Sending request to OpenAI API")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model=model_name,
        max_tokens=max_tokens
    )

    response = chat_completion.choices[0].message.content
    logging.info("Received response from OpenAI API")
    return response

import tiktoken

def count_tokens(text, model_name="gpt-4"):
    # Initialize the encoder for the specified model
    encoder = tiktoken.encoding_for_model(model_name)

    # Encode the text to get the tokens
    tokens = encoder.encode(text)

    # Return the number of tokens
    return len(tokens)

def count_tokens_in_csv(file_path, model_name="gpt-4o"):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert all columns to string and concatenate all data into a single string
    text = df.astype(str).agg(' '.join, axis=1).str.cat(sep=' ')

    # Initialize the encoder for the specified model
    encoder = tiktoken.encoding_for_model(model_name)

    # Encode the text to get the tokens
    tokens = encoder.encode(text)

    # Return the number of tokens
    return len(tokens)


if __name__ == '__main__':
    # Example usage
    text = pd.read_csv('./data/series/source/all_sources_combined.csv')
    model_name = "gpt-4o"  # Change this if using a different model
    num_tokens = count_tokens_in_csv(text, model_name)
    
    print(f"Number of tokens: {num_tokens}")

