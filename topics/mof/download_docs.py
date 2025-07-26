from utils import download_file
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

download_dir = "./docs"  # all downloads go here
os.makedirs(download_dir, exist_ok=True)

base_url = "https://www.mofed.gov.et"
dirs = [
    "budget",
    "bulletin",
    "audit-report",
    "tax-policy",
    "investment-laws",
    "proclamation",
    "fta-resource",
    "resources-by-directorate",
]



def fetch_links(url):
    """Fetch all relevant links from the given URL."""
    try:
        resp = urlopen(url, timeout=10)
        soup = BeautifulSoup(resp, "html.parser")
        links = soup.find_all("a", class_="fa")

        if not links:
            other_links = [
                u.get("href") for u in soup.find("div", class_="col").find_all("a")
            ]
            for link in other_links:
                rurl = base_url + link
                try:
                    rresp = urlopen(rurl, timeout=10)
                    rsoup = BeautifulSoup(rresp, "html.parser")
                    links.extend(rsoup.find_all("a", class_="fa"))
                except Exception as e:
                    print(f"Error fetching nested URL {rurl}: {e}")

        return [base_url + link.get("href") for link in links if link.get("href")]
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return []


def main(urls):
    for url in urls:
        full_url = base_url + url
        links = fetch_links(full_url)

        if not links:
            print(f"No links found for {full_url}")
            continue

        ddir = os.path.join(download_dir, os.path.basename(url.rstrip("/")))
        os.makedirs(ddir, exist_ok=True)

        for link in links:
            file_path = os.path.join(ddir, os.path.basename(link))
            if not os.path.exists(file_path):
                print(f"Downloading {link} ...")
                try:
                    download_file(link, file_path)
                except Exception as e:
                    print(f"Error downloading file {link}: {e}")


if __name__ == "__main__":
    urls = [f"/resources/{url}/" for url in dirs]
    main(urls)
