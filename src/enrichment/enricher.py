import pandas as pd

from src.enrichment.openai_client import (
    analyze_company
)


def enrich_dataframe(df):

    results = []

    total = len(df)

    for idx, row in df.iterrows():

        print(f"\nAnalyzing {idx+1}/{total}")

        try:

            enrichment = analyze_company(row)

            results.append(enrichment)

        except Exception as e:

            print(f"ERROR: {e}")

            results.append({})

    enrichment_df = pd.DataFrame(results)

    final_df = pd.concat(
        [df.reset_index(drop=True), enrichment_df],
        axis=1
    )

    return final_df