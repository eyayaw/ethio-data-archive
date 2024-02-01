import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def scrape_category(category_url):
    base_url = 'http://csa.gov.et'

    # s = requests.Session()
    response = s.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.select_one("#phoca-dl-category-box > div.pd-category > h3").text.strip()
    # find all the subcategory links on the current page
    subcategories = soup.select(".pd-category > .pd-subcategory > a[href]")

    if len(subcategories) > 0:
        # if there are subcategories, recursively scrape each one
        pdf_links = {title: {}}
        for subcategory in subcategories:
            subcategory_url = urljoin(base_url, subcategory['href'])
            subcategory_pdf_links = scrape_category(subcategory_url)
            for subcategory_title, subcategory_links in subcategory_pdf_links.items():
                pdf_links[title].update({subcategory_title: subcategory_links})
    else:
        # if there are no subcategories, find all PDF links on the current page
        pdf_links_list = soup.select("div.pd-filenamebox > div.pd-filename > div > div.pd-float > a[href]")

        # extract the links of each PDF document
        pdf_links = {title: {pdf_link.text: urljoin(base_url, pdf_link['href']) for pdf_link in pdf_links_list}}
    return pdf_links


# params
base_url = 'http://csa.gov.et'
category_url = f"{base_url}/survey-report/category/14-all-survey-reports"
s = requests.Session()

response = s.get(category_url)
soup = BeautifulSoup(response.content, 'html.parser')
category = soup.select_one("#phoca-dl-category-box > div.pd-category > h3").text.strip()
subcats = soup.select(".pd-category > .pd-subcategory > a[href]")
subcats_links = {link.text.strip(): urljoin(base_url, link['href']) for link in subcats}


# download all pdfs in each subcategory
pdf_links = {}
os.makedirs("./csa-surveys", exist_ok=True)
for subcat, subcat_link in subcats_links.items():
    os.makedirs(f"./csa-surveys/{category}/{subcat}", exist_ok=True)
    pdf_links.update(scrape_category(subcat_link))



# flattens a nested dictionary by joining keys at each depth with a separator
def flatten_dict(d, parent_key= '', sep = '.') -> dict:
    items = []
    for k, v in d.items():
        # concatenate the parent key and current key with the separator
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            # recursively flatten nested dictionaries and extend the result to the items list
            nested_items = flatten_dict(v, new_key, sep=sep).items()
            items.extend(nested_items)
        else:
            # add the flattened key-value pair to the items list
            items.append((new_key, v))
    # return the flattened dictionary as a dictionary
    return dict(items)


pdf_links_flat = flatten_dict(pdf_links, sep="||")

# save all pdf links to a file
for k, v in pdf_links_flat.items():
    keys = k.split("||")
    dirname = f"./csa-surveys/{category}/" + "/".join(keys[:-1])
    filename = keys[-1]
    os.makedirs(dirname, exist_ok=True)
    with open(f"{dirname}/{filename}", "wb") as f:
        res = requests.get(v)
        try:
            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        except Exception as e:
            print(f"Error: {e}")
