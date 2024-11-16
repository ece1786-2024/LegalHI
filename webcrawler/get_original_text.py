import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import random
import json


def scrape_original_text(df):
    data = {}
    new_df = df.copy()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
    ]
    for idx, row in df.iterrows():
        url = row['keys']
        citation = row['citation']
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            ps = soup.find_all('p', class_='SCCNormalDoubleSpacing', style="margin-bottom:24.0pt")
            original_text = ''
            for p in ps:
                original_text += p.get_text()

            data[idx] = {
                "original_text": original_text,
                "original_key": row['keys'],
                "citation": citation
            }
        except:
            data[idx] = {
                "original_text": "ERROR",
                "original_key": row['keys'],
                "citation": citation
            }
        print(data[idx])
        # Save after each iteration to avoid losing data in case of failure
        with open("original_text_2.json", "w") as f:
            json.dump(data, f, indent=4)

        # update original_keys.csv each iteration in case of failure
        new_df = new_df.drop(index=new_df.index[0])
        new_df.to_csv("original_keys.csv")

        time.sleep(random.uniform(2, 5))


# Load the CSV with keys
df_keys = pd.read_csv("original_keys.csv")
scrape_original_text(df_keys)