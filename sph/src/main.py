from re import M
from crowdtangle_api import authorization, generate_data
from data_processing import format_crowdtangle_data, convert_accounts
from analysis import make_png_one, analysis_two, analysis_one
import schedule
import time
from datetime import datetime, timedelta
import os


def main():
    key = "UxA6YGlZCS5h2YY3GIa9IUOaC1Te5XqArv6nhp2q"

    # Authorization and data retrieval
    result_df = format_crowdtangle_data(authorization(key))

    # Data processing and analysism

    folder_name = 'crowdtangle'
    current_directory = os.getcwd()
    # Create the full path for the new folder
    folder_path = os.path.join(current_directory, folder_name)
    print(folder_path)
    yesterday = datetime.now() - timedelta(days=1)
    start_date = yesterday.strftime('%Y%m%d')
    print(start_date)
    end_date = datetime.now().strftime('%Y%m%d')
    print(end_date)
    combined_df = generate_data(folder_path, start_date, end_date)
    combined_df['account'] = combined_df['account'].str.replace(
        "True", "'True'")

    # Further data processing
    combined_df['name'] = convert_accounts(combined_df)

    # Perform analyses
    analysis_two(combined_df)
    df_one, df_two = analysis_one(combined_df)
    make_png_one(df_one)


def manual_run():
    print("Running the script manually...")
    main()


if __name__ == "__main__":
    schedule.every().day.at("12:00").do(main)

    while True:
        print("Press 'm' to run the script manually or 'q' to quit.")
        choice = input()

        if choice.lower() == 'm':
            manual_run()
        elif choice.lower() == 'q':
            print("Quitting the script.")
            break
        else:
            print("Invalid choice. Try again.")

        schedule.run_pending()
        time.sleep(1)
