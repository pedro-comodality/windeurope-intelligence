import json
import time
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# AI PROFILE ANALYSIS
# =====================================================

def analyze_company(row):

    try:

        company = row.get("company", "")
        category = row.get("product_category", "")
        generation = row.get("generation_type", "")
        website_text = row.get("website_text", "")

        prompt = f"""
You are a senior offshore wind industry analyst.

Analyze this company.

COMPANY:
{company}

CATEGORY:
{category}

GENERATION:
{generation}

WEBSITE CONTENT:
{website_text[:6000]}

Return ONLY valid JSON.

{
    "segment": "",
    "offshore_maturity": 0,
    "floating_readiness": 0,
    "epc_strength": 0,
    "innovation_score": 0,
    "digitalization_score": 0,
    "strategic_fit": 0,
    "growth_potential": 0,
    "market_presence": 0,
    "recommended_priority": "",
    "summary": ""
}

Scoring rules:
- 0-100
- offshore expertise matters heavily
- floating wind expertise matters heavily
- EPC capabilities are strategic
- innovation and digitalization are important
- ports/logistics/maritime are relevant
- predictive maintenance and AI are valuable
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content

        result = json.loads(content)

        return result

    except Exception as e:

        print(f"ERROR profiling company: {e}")

        return {}


# =====================================================
# DATAFRAME ENRICHMENT
# =====================================================

def enrich_profiles(df):

    profiles = []

    total = len(df)

    for idx, row in df.iterrows():

        print(f"\nProfiling {idx+1}/{total}")

        profile = analyze_company(row)

        profiles.append(profile)

        time.sleep(1)

    profiles_df = pd.DataFrame(profiles)

    df = pd.concat(
        [df.reset_index(drop=True), profiles_df],
        axis=1
    )

    return df