import requests
import trafilatura
import pandas as pd
import time


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


# =====================================================
# DOWNLOAD WEBSITE TEXT
# =====================================================

def scrape_website(url):

    if not url:
        return ""

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            return ""

        downloaded = trafilatura.extract(
            response.text,
            include_links=False,
            include_images=False
        )

        if not downloaded:
            return ""

        # limitar tamaño
        downloaded = downloaded[:8000]

        return downloaded

    except Exception:

        return ""


# =====================================================
# ENRICH DATAFRAME
# =====================================================

def scrape_websites(df):

    website_texts = []

    total = len(df)

    for idx, row in df.iterrows():

        print(f"\nScraping {idx+1}/{total}")

        url = row.get("website", "")

        text = scrape_website(url)

        website_texts.append(text)

        time.sleep(1)

    df["website_text"] = website_texts

    return df