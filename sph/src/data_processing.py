# data_processing.py

import pandas as pd
import json
from datetime import datetime
import os
import re


def check_folder(folder_name):
    documents_path = os.path.expanduser('~/Documents')
    folder_path = os.path.join(documents_path, 'crowdtangle')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created in Documents.")
    else:
        print(f"Folder '{folder_name}' already exists in Documents.")


def format_crowdtangle_data(result_df, folder_name='crowdtangle'):
    check_folder(folder_name)
    # formatting the data the data is a list of dictionaries
    # there are total of 10 posts
    # each post may or may not have same column, if there are missing column, lets fill it with 0

    all_keys = set()
    for post in result_df["result"]["posts"]:
        all_keys.update(post.keys())

    for dict_post in result_df["result"]["posts"]:
        for key in all_keys - set(dict_post.keys()):
            dict_post[key] = 0

    current_date = datetime.now().strftime("%Y%m%d")
    for dict_post in result_df["result"]["posts"]:
        dict_post["date_run"] = current_date
    folder_path = os.path.join(os.path.expanduser(
        '~/Documents/sph/src'), folder_name)
    csv_file_path = os.path.join(
        folder_path, f"crowdtangle_data_{current_date}.csv")
    pd.DataFrame(result_df["result"]["posts"]).to_csv(
        csv_file_path, index=False, encoding='utf-8')

    return result_df["result"]["posts"]


def convert_s_quotes(input_string):
    # Define a regular expression pattern to match strings ending with "s"
    pattern = r'(\w+)"s\b'

    # Define a replacement function to convert "s" to 's
    def replace_match(match):
        return match.group(1) + "'s"

    # Use re.sub() to perform the replacement
    result_string = re.sub(pattern, replace_match, input_string)

    return result_string


def convert_accounts(combined_df):
    new_col_data = []

    for account_string in combined_df["account"]:
        print(account_string)
        result = account_string.replace("'", '"')
        print(account_string)
        result = convert_s_quotes(result)

        print(result)

        # convert back to string, replacing double quotes with single quotes, except for 's
        try:
            data = json.loads(result)

            new_col_data.append(data["name"])
        except json.decoder.JSONDecodeError as e:
            # Print the problematic substring
            error_location = e.pos
            print(f"JSONDecodeError: {e}")
            print(
                f"Problematic substring: {result[max(0, error_location-10):error_location+10]}")
            new_col_data.append("Error in JSONDecode")

    combined_df['name'] = new_col_data
    return combined_df['name']
