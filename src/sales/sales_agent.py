from openai import OpenAI
from dotenv import load_dotenv

import os
import pandas as pd


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# PROMPT
# =====================================================

def build_sales_prompt(row):

    return f"""
You are a senior offshore wind business developer.

Analyze this company and generate:

1. Strategic summary
2. Why this company matters
3. Commercial opportunity
4. Suggested partnership angle
5. Personalized outreach email

COMPANY:
{row.get("company", "")}

COUNTRY:
{row.get("country", "")}

PRODUCT CATEGORY:
{row.get("product_category", "")}

WEBSITE INFO:
{row.get("website_text", "")}

SEGMENT:
{row.get("segmento", "")}

TECH LEVEL:
{row.get("nivel_tecnologico", "")}

OFFSHORE:
{row.get("offshore", "")}

FLOATING WIND:
{row.get("floating_wind", "")}

EPC:
{row.get("epc", "")}

INNOVATION:
{row.get("innovacion", "")}

GROWTH:
{row.get("crecimiento", "")}
"""


# =====================================================
# AI SALES ANALYSIS
# =====================================================

def analyze_company(row):

    try:

        prompt = build_sales_prompt(row)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite B2B offshore wind sales strategist."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"ERROR: {str(e)}"


# =====================================================
# DATAFRAME ENRICHMENT
# =====================================================

def enrich_sales(df):

    sales_outputs = []

    total = len(df)

    for idx, (_, row) in enumerate(df.iterrows()):

        print(f"\nSales AI {idx+1}/{total}")

        result = analyze_company(row)

        sales_outputs.append(result)

    df["sales_strategy"] = sales_outputs

    return df