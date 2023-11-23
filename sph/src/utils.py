# utils.py

import os
from datetime import datetime


def check_folder(folder_name):
    documents_path = os.path.expanduser('~/Documents')
    folder_path = os.path.join(documents_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created in Documents.")
    else:
        print(f"Folder '{folder_name}' already exists in Documents.")


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


def format(result_df, folder_name='crowdtangle'):
    check_folder(folder_name)

    all_keys = set()
    for post in result_df["result"]["posts"]:
        all_keys.update(post.keys())

    for dict_post in result_df["result"]["posts"]:
        for key in all_keys - set(dict_post.keys()):
            dict_post[key] = 0

    current_date = datetime.now().strftime("%Y%m%d")
    for dict_post in result_df["result"]["posts"]:
        dict_post["date_run"] = current_date
    folder_path = os.path.join(os.path.expanduser('~/Documents'), folder_name)
    csv_file_path = os.path.join(
        folder_path, f"crowdtangle_data_{current_date}.csv")
    pd.DataFrame(result_df["result"]["posts"]).to_csv(
        csv_file_path, index=False, encoding='utf-8')

    return result_df["result"]["posts"]
