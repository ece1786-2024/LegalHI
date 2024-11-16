import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import random

def scrape_scc_cases(url):
    # Send an HTTP request to the webpage
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the relevant sections using specified classes
    body = soup.find('body')
    web_core_sec = body.find('div', id='wb-body-sec')
    web_core = web_core_sec.find('div', id='wb-core')
    wb_core_in = web_core.find('div', id='wb-core-in')
    wb_main = wb_core_in.find('div', id='wb-main')
    span_6 = wb_main.find_all('div', class_='span-6')[0]
    tabs_panel = span_6.find('div', class_='tabs-panel')
    years = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    links = []
    for year in years:
        tmp_data = tabs_panel.find('div', id=year)
        table_data = tmp_data.find('table')
        for row in table_data.find_all('tr'):
            cells = row.find_all(['td'])
            if not cells: continue
            link_tag = row.find('a')
            if link_tag and link_tag.has_attr('href'):
                href = link_tag['href']
                if href[0]!="/": links.append(href)
    return links

def scrape_scc_summary(links):
    base_url = "https://www.scc-csc.ca/case-dossier/cb/"
    df = pd.DataFrame()
    citations = []
    summarys = []
    count = 0
    for link in links:
        target_url = base_url + link
        while True:
            try:
                response = requests.get(target_url)
                response.raise_for_status()  # Will raise an error for 4xx/5xx status codes
                break  # Exit loop if request is successful
            except requests.exceptions.HTTPError as err:
                print(f"Error occurred: {err}. Retrying...")
                time.sleep(60)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('body')
        web_core_sec = body.find('div', id='wb-body-sec')
        web_core = web_core_sec.find('div', id='wb-core')
        wb_core_in = web_core.find('div', id='wb-core-in')
        wb_main = wb_core_in.find('div', id='wb-main')
        wb_main_in = wb_main.find('div', id='wb-main-in')
        # get related info
        info_div = wb_main_in.find('div', class_='span-2 float-right font-small margin-bottom-medium')
        info_div_sec = info_div.find('div', class_='module-note module-simplify margin-top-none')
        info_ul = info_div_sec.find('ul')
        li = info_ul.find_all('li', class_="line-height-medium")
        try:
            citation = str(li).split("Neutral Citation</strong>:")[1].split("<")[0].strip()
        except:
            citation = "error:" + target_url

        # get text
        try:
            ps = wb_main_in.find_all('p', class_=None, recursive=False)
            summary_text = ""
            for p in ps:
                # remove <p> and <\p>
                p = str(p).replace("<p>", "").replace("</p>", "")
                summary_text += p
        except:
            summary_text = "error:" + target_url
        citations.append(citation)
        summarys.append(summary_text)
        count += 1
        if count % 20 == 0:  # Report every 20 links
            print(f"Processed {count}/{len(links) } links.")
        time.sleep(random.uniform(2, 5))
    print("Processed all links. Converting to csv")
    df['citation'] = citations
    df['summary'] = summarys
    df.to_csv("scc_summary.csv", index=False)

# # URL of the Supreme Court of Canada case information page
url = "https://www.scc-csc.ca/case-dossier/cb/index-eng.aspx"
links = scrape_scc_cases(url)
df = pd.DataFrame(links, columns=["links"])
df.to_csv("links.csv", index=False)
