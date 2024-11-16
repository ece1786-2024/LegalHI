import pandas as pd
import random
import time
import requests
from bs4 import BeautifulSoup


def scrape_scc_summary(links):
    total_len = len(links)
    base_url = "https://www.scc-csc.ca/case-dossier/cb/"
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

        # Get related info
        info_div = wb_main_in.find('div', class_='span-2 float-right font-small margin-bottom-medium')
        info_div_sec = info_div.find('div', class_='module-note module-simplify margin-top-none')
        info_ul = info_div_sec.find('ul')
        li = info_ul.find_all('li', class_="line-height-medium")
        try:
            citation = str(li).split("Neutral Citation</strong>:")[1].split("<")[0].strip()
        except:
            citation = "error:" + target_url

        # Get text
        try:
            ps = wb_main_in.find_all('p', class_=None, recursive=False)
            summary_text = ""
            for p in ps:
                # Remove <p> and <\p>
                p = str(p).replace("<p>", "").replace("</p>", "")
                summary_text += p
        except:
            summary_text = "error:" + target_url

        citations.append(citation)
        summarys.append(summary_text)
        count += 1

        if count % 20 == 0:  # Report every 20 links
            print(f"Processed {count}/{total_len} links.")

        # Update CSV after every iteration
        df = pd.DataFrame({'citation': citations, 'summary': summarys})
        df.to_csv("scc_summary_3.csv", index=False)

        # Remove the processed link from the original list and save it back to CSV
        new_links = links[count:]
        pd.DataFrame(new_links, columns=["links"]).to_csv("links.csv", index=False)

        time.sleep(random.uniform(2, 5))

    print("Processed all links.")


# Read the links and start scraping
links_df = pd.read_csv("links.csv")
links = links_df['links'].tolist()
scrape_scc_summary(links)
