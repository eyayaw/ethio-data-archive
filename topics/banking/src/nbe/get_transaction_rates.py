import csv
import os
import requests
from datetime import datetime, timedelta
import time

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}


def get_transaction_rates(date: str):
    params = {"date": date}
    try:
        response = requests.get(
            "https://api.nbe.gov.et/api/filter-transaction-exchange",
            params=params,
            headers=headers,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []  # Return an empty list on error

    data = response.json().get("data", [])
    if not data:
        print(f"No exchange rate data available for {date}.")
    return data


def extract_data(data):
    # Clean and structure the data
    cleaned_data = [
        {
            "currency_id": item["currency"]["id"],
            "currency_name": item["currency"]["name"],
            "currency_code": item["currency"]["code"],
            "date": item["date"],
            "buying": item["buying"],
            "selling": item["selling"],
        }
        for item in data
    ]

    return cleaned_data


# Write the cleaned data to a CSV file
def save_data(data, path):
    mode = "a" if os.path.exists(path) else "w"
    fieldnames = data[0].keys() if data else []

    with open(path, mode=mode, newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()  # Write the header only for new files
        writer.writerows(data)    # Write multiple rows


if __name__ == "__main__":
    end_date = datetime.today()
    start_date = transaction_date = datetime.fromisoformat("2024-08-09")
    transaction_data = []
    while True:
        data = get_transaction_rates(transaction_date.strftime("%Y-%m-%d"))
        if transaction_date > end_date:  # if not data:
            break
        transaction_data.extend(extract_data(data))
        transaction_date += timedelta(days=1)
        time.sleep(2)

    csv_path = f"data/nbe/transaction_data_{start_date:%Y-%m-%d}_{end_date:%Y-%m-%d}.csv"
    save_data(transaction_data, csv_path)
