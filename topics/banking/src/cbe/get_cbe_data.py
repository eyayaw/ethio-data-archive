import json
import os
import requests


headers = {
    "Host": "www.combanketh.et",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_data(session, endpoint, params):
    response = session.get(endpoint, headers=headers, params=params, verify=False)
    data = response.json()
    return data


def dump_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    session = requests.Session()
    endpoint_list = [
        "https://www.combanketh.et/cbeapi/branches",
        "https://www.combanketh.et/cbeapi/pos",
        "https://www.combanketh.et/cbeapi/cbe-birr-agents",
        "https://www.combanketh.et/cbeapi/cbe-noor-branches",
    ]
    params_list = [{"_limit": "", "_sort": "name"}] * len(endpoint_list)
    for endpoint, params in zip(endpoint_list, params_list):
        data = get_data(session, endpoint, params)
        filename = f"data/cbe/{os.path.basename(endpoint)}.json"
        dump_json(data, filename)


if __name__ == "__main__":
    main()
