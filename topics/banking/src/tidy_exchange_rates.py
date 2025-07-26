import json
from pathlib import Path
from typing import Optional
import pandas as pd

CBE_DATA_DIR = Path("data/cbe/exchange-rates/")
CBE_TIDY_DATA_PATH = "data/exchange_rates_cbe.csv"
CBE_DATA_GLOB = "*.json"

NBE_DATA_DIR = Path("data/nbe/")
NBE_TIDY_DATA_PATH = "data/exchange_rates_nbe.csv"
NBE_DATA_GLOB = "transaction_data*.csv"

# from CBE ----


def tidy_cbe() -> Optional[pd.DataFrame]:
    """
    Reads all the data JSON files in the directory, tidy the daily exchange rates and write unique data points to csv.
    """
    if not CBE_DATA_DIR.exists():
        raise FileNotFoundError(f"Directory {CBE_DATA_DIR} not found.")

    files = list(CBE_DATA_DIR.glob(CBE_DATA_GLOB))
    if not files:
        print(F"Check whether the glob {CBE_DATA_GLOB} is correct.")
        return None

    data = []
    for file in files:
        try:
            with open(file, "r") as f:
                chunks = json.load(f)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue
        for entry in chunks:
            daily_rates = _flatten_daily_cbe(entry)
            data.extend(daily_rates)

    data = pd.DataFrame(data)
    # there are duplicates because of (start_date, end_date)
    data = data.drop_duplicates()
    data = data.sort_values("date")

    data.to_csv(CBE_TIDY_DATA_PATH, index=False)

    return data


def _flatten_daily_cbe(entry: dict) -> list:
    common = {
        "date": entry.get("Date"),
        "published_at": entry.get("published_at"),
        # "created_at": entry.get("createdAt"),
        # "updated_at": entry.get("updatedAt"),
    }
    daily_rates = []

    for exchange_rate in entry["ExchangeRate"]:
        currency = exchange_rate.get("currency", {})
        data = {
            **common,
            "CurrencyCode": currency.get("CurrencyCode"),
            "CurrencyName": currency.get("CurrencyName"),
            "CashBuying": exchange_rate.get("cashBuying"),
            "CashSelling": exchange_rate.get("cashSelling"),
            "TransactionalBuying": exchange_rate.get("transactionalBuying"),
            "TransactionalSelling": exchange_rate.get("transactionalSelling"),
        }
        daily_rates.append(data)
    return daily_rates


# from NBE ----


def tidy_nbe() -> Optional[pd.DataFrame]:
    if not NBE_DATA_DIR.exists():
        raise FileNotFoundError(f"Dir {NBE_DATA_DIR} does not exist.")
    files = list(NBE_DATA_DIR.glob(NBE_DATA_GLOB))
    if not files:
        print(F"Check whether the glob {NBE_DATA_GLOB} is correct.")
        return None
    data = []
    for file in files:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            print(f"Error processing {file=}: {e}")
        data.append(df)
    if not data:
        return None
    data = pd.concat(data, axis="rows")

    data = data.drop_duplicates()
    data = data.sort_values("date")

    data.to_csv(NBE_TIDY_DATA_PATH, index=False)
    return data


if __name__ == "__main__":
    tidy_cbe()
    tidy_nbe()
