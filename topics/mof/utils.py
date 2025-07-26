from urllib.request import urlretrieve
import os


def download_file(url, path=None):
    if not path:
        path = os.path.basename(url)
    if os.path.exists(path):
        print("The file exists, download skipped.")
    else:
        try:
            print(f"Downloading {url} to {path}")
            urlretrieve(url, path)
            print("Download finished.")
        except Exception as e:
            print(f"Download did not successed.\n{e}")