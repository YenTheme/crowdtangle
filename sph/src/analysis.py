# analysis.py

import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
import re


def convert_s_quotes(input_string):
    # Define a regular expression pattern to match strings ending with "s"
    pattern = r'(\w+)"s\b'

    # Define a replacement function to convert "s" to 's
    def replace_match(match):
        return match.group(1) + "'s"

    # Use re.sub() to perform the replacement
    result_string = re.sub(pattern, replace_match, input_string)

    return result_string


def analysis_one(combined_df):
    # answer three main questions
    # how many publications does sph manage
    publications = ['The Straits Times', 'Lianhe Zhaobao 联合早报', 'The Business Times', 'Her World', "Harper's BAZAAR Singapore", 'Tamil Murasu', 'The Peak', 'Nuyou', 'Berita Harian', 'Home & Decor', 'FEMALE', 'Shin Min Daily News', 'MONEY FM 89.3',
                    '96.3好FM', 'Awedio', 'ONE FM 91.3', 'Kiss92 FM', 'ICON', 'The New Paper', "The Singapore Women's Weekly", 'HardwareZone', 'HeyKaki', 'Uweekly', 'UFM100.3', 'tabla!', 'Health No.1', 'Stomp', 'Baalar Murasu', 'Cilik Cerdik', 'Gen G', 'IN', 'Little Red Dot', 'Maanavar Murasu', 'Thumbs Up', 'Thumbs Up Junior', 'Thumbs Up Little Junior']

    no_pub_managed = len(publications)
    # creating dataframs for perf of posts

    # performance for posts managed by these publications
    # formating the dataframe
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

    ratings_dict = []
    for ratings in combined_df['statistics']:
        data = ratings.replace("'", '"')
        result = json.loads(data)
        ratings_dict.append(result)

    combined_df['ratings'] = ratings_dict

    combined_df['title'] = combined_df["name"].astype(
        str) + ":" + combined_df["title"]
    df_one = pd.concat([combined_df['title'], combined_df['ratings']], axis=1)
    df_two = pd.concat([combined_df['name'], combined_df['ratings']], axis=1)

    return df_one, df_two


def make_png_one(df_one):
    for title in range(len(df_one['title'])):
        columns = list(df_one['ratings'][title]['actual'].keys())
        index = []
        rows_data = []
        for rows in df_one['ratings'][title]:
            index.append(rows)
            row = list(df_one['ratings'][title][rows].values())
            rows_data.append(row)
        df = pd.DataFrame(rows_data, columns=columns, index=index)

        df_plotly = df.reset_index().melt(
            id_vars='index', var_name='Reaction', value_name='Count')

        # Plotting
        fig = px.bar(df_plotly, x='Reaction', y='Count', color='index', text='Count',
                     labels={'index': 'Category'}, title='Actual vs Expected Reactions:' + df_one['title'][title], barmode='group')
        fig.update_traces(textposition='outside')
        date = datetime.now().strftime("%Y%m%d")
        directory = "~/Documents/sph/src/crowdtangle"

        # Convert the tilde (~) to the full path
        directory = os.path.expanduser(directory)
        # file_path = os.path.join(directory, f"plot_{title}_{date}.png")

        # Check if the directory exists, create it if not
        os.makedirs(directory, exist_ok=True)
        # fig.write_image(file_path)
        img_bytes = pio.to_image(fig,format="png", engine="orca")
        # You can then save the bytes to a file or do further processing
        with open(f"plot_{title}_{date}.png", "wb") as f:
            f.write(img_bytes)

    return


def analysis_two(combined_df):
    df_three = pd.concat(
        [combined_df['name'], combined_df['subscriberCount']], axis=1)

    df_grouped = df_three.drop_duplicates()

    fig_two = px.bar(df_grouped, x='name', y='subscriberCount',
                     text='subscriberCount', title='Subscribers per publisher', barmode='group')
    fig_two.update_traces(textposition='outside')
    date = datetime.now().strftime("%Y%m%d")
    directory = "~/Documents/sph/src/crowdtangle"

    # Convert the tilde (~) to the full path
    directory = os.path.expanduser(directory)
    # file_path = os.path.join(directory, f"plot_subscriberCount_{date}.png")

    # Check if the directory exists, create it if not
    os.makedirs(directory, exist_ok=True)
    img_bytes = pio.to_image(fig_two,format="png", engine="orca")
    # You can then save the bytes to a file or do further processing
    with open(f"plot_subscriberCount_{date}.png", "wb") as f:
        f.write(img_bytes)

    return

