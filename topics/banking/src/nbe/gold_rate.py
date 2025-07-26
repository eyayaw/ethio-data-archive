from datetime import date
import requests

headers = {
    "Host": "market.nbebank.com",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
}


url = "https://market.nbebank.com/admin/searchsystem/goldrate/gold_ratelist.php"
def get_gold(from_date, to_date):
    params = {
        "x_time": from_date,
        "y_time": to_date,
        "z_time": "BETWEEN",
        "export": "csv",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        verify=False,
    )

    with open("data/goldrate_data.csv", "wb") as f:
        f.write(response.content)

    return response.text


def main():
    from_date = "2009/01/01/"
    to_date = date.today().strftime("%Y/%m/%d")
    gold_data = get_gold(from_date, to_date)
    print(gold_data)

if __name__ == "__main__":
    main()