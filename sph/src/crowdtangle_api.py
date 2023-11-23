import requests
from time import sleep
import pandas as pd
from datetime import datetime
import os


def make_crowdtangle_request(url, params):
    retries = 3
    delay = 20  # seconds

    for _ in range(retries):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        print(f"Error {response.status_code}: {response.text}")
        print(f"Retrying in {delay} seconds...")
        sleep(delay)

    raise Exception(
        "Failed to retrieve data from CrowdTangle after multiple attempts.")


def authorization(key):
    url = 'https://api.crowdtangle.com/posts'
    params = {'token': key}
    current_date = datetime.now().strftime('%Y%m%d')

    try:
        data = make_crowdtangle_request(url, params)

        if data:
            df = pd.DataFrame(data)
            return df

        else:
            print("No data retrieved from CrowdTangle.")
            return None

    except requests.exceptions.RequestException as e:
        # handle errors (print or log error message)
        print(f"Error fetching data from CrowdTangle: {e}")
        return None


def generate_data(folder_path, start_date, end_date):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    dataframes = []

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path, encoding='utf-8')

        df['date_run'] = pd.to_datetime(df['date_run'], format='%Y%m%d')
        df = df[(df['date_run'] >= start_date) & (df['date_run'] <= end_date)]

        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df
