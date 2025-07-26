import requests
from datetime import datetime


def get_interbank_exchange_rates(date=None, export_format="csv"):
    if date is None:
        date = datetime.now().strftime("%m/%d/%Y")

    url = "https://market.nbebank.com/admin/searchsystem/interbank/interbank_dailylist.php"
    headers = {"cookie": "PHPSESSID=up6ic06h1ii978dkkr0if1sqh2"}
    params = {"x_time": date, "z_time": "<", "export": export_format}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    return response


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"nbe/data/interbank_exchange_rates_{timestamp}.csv"
    response = get_interbank_exchange_rates()

    if response and response.content:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print("No content to write to file")


if __name__ == "__main__":
    main()
