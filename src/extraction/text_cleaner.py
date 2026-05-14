import re
import pandas as pd
from rapidfuzz import fuzz


def clean_company_name(name):

    if pd.isna(name):
        return ""

    # eliminar numeración PDF
    name = re.sub(r"\d+\s*/\s*\d+", "", name)

    # eliminar espacios múltiples
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def clean_website(url):

    if pd.isna(url):
        return ""

    url = url.strip()

    url = url.replace(" ", "")

    return url


def normalize_generation_type(text):

    if pd.isna(text):
        return ""

    return text.lower().strip()


def normalize_product_category(text):

    if pd.isna(text):
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def deduplicate_companies(df):

    seen = []
    rows = []

    for idx, row in df.iterrows():

        company = row["company"]

        normalized = company.lower()

        duplicate = False

        for existing in seen:

            similarity = fuzz.ratio(
                normalized,
                existing
            )

            if similarity > 95:
                duplicate = True
                break

        if not duplicate:

            seen.append(normalized)

            rows.append(idx)

    return df.loc[rows].reset_index(drop=True)


def clean_dataframe(df):

    df["company"] = df["company"].apply(
        clean_company_name
    )

    df["website"] = df["website"].apply(
        clean_website
    )

    df["generation_type"] = df[
        "generation_type"
    ].apply(normalize_generation_type)

    df["product_category"] = df[
        "product_category"
    ].apply(normalize_product_category)

    df = deduplicate_companies(df)

    return df