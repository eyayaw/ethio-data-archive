import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

csa_url = "https://www.statsethiopia.gov.et/Our-Survey-Reports"
session = requests.Session()
res = session.get(csa_url, verify=False)
soup = BeautifulSoup(res.text, "html.parser")

pdf_files = []

for link in soup.find_all('a'):
    if link.get('href').endswith('.pdf'):
        pdf_files.append(link.get('href'))

pdf_files = sorted(pdf_files, key=lambda x: os.path.basename(x))
pdf_files = [pdf.replace("http//", "http://") for pdf in pdf_files]
pdf_files = [pdf.replace("https//", "https://") for pdf in pdf_files]

for pdf in pdf_files:
    fpath = pdf.split("wp-content/")[-1]
    dirname = os.path.join("./csa-surveys/", os.path.dirname(fpath))
    os.makedirs(dirname, exist_ok=True)
    fpath = os.path.join(dirname,os.path.basename(fpath))
    if not os.path.exists(fpath):
        try:
            with open(fpath, 'wb') as f:
                res = requests.get(pdf, verify=False, timeout=5)
                res.raise_for_status()
                f.write(res.content)
        except requests.exceptions.RequestException as e:
            print(f'Failed to download:{pdf}, {e}')
            