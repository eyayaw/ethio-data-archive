import time
import requests
from datetime import date, timedelta
import json
import os

# disable insecurerequestwarning
requests.packages.urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}


# get cbe's business dates, only takes sundays as non business days
# TODO: remove public holidays too
def get_business_dates(from_date, to_date):
    dates = []
    current_date = from_date
    while current_date <= to_date:
        if current_date.weekday() != 6:  # 6 for sunday
            dates.append(current_date)
        current_date += timedelta(days=1)
    return dates


def get_daily_exchange_rates(session, date, limit=1):
    endpoint = "https://www.combanketh.et/cbeapi/daily-exchange-rates"
    params = {
        "_limit": str(limit),
        "_sort": "Date:DESC",
        "Date": str(date),
    }
    # NB: we need to disable SSL certificate verification
    try:
        response = session.get(endpoint, headers=headers, params=params, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error has occurred: {e}")
        return None
    else:
        rates_data = response.json()
        if not rates_data:
            print(f"Looks like there is no exchange rates data for {date}.")
        return rates_data



def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def main():
    session = requests.Session()
    from_date = date(2024, 12, 13)
    to_date = date.today()
    dates = get_business_dates(from_date, to_date)
    data = []

    for business_date in dates:
        exchange_rates = get_daily_exchange_rates(session, business_date)
        if exchange_rates:
            data.extend(exchange_rates)
        time.sleep(1)
    if data:
        filename = f"data/cbe/exchange-rates/exchange_rates_{from_date}_{to_date}.json"
        save_json(data, filename)


if __name__ == "__main__":
    main()
