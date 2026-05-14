from openai import OpenAI
from dotenv import load_dotenv

import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# RELATIONSHIP ANALYSIS
# =====================================================

def build_relationship_prompt(target_company, df):

    company_list = []

    for _, row in df.iterrows():

        company_list.append(
            f"""
Company: {row.get('company', '')}
Category: {row.get('product_category', '')}
Segment: {row.get('segmento', '')}
Offshore: {row.get('offshore', '')}
Floating: {row.get('floating_wind', '')}
EPC: {row.get('epc', '')}
"""
        )

    companies_text = "\n".join(company_list[:50])

    return f"""
You are a senior offshore wind strategy consultant.

Analyze this target company:

TARGET:
{target_company}

And identify:

1. Similar companies
2. Potential strategic partners
3. Competitive threats
4. Supply chain synergies
5. Floating wind relevance
6. EPC ecosystem relevance

COMPANIES DATABASE:
{companies_text}

Return concise strategic insights.
"""


# =====================================================
# GENERATE RELATIONSHIP ANALYSIS
# =====================================================

def generate_relationship_analysis(
    target_company,
    df
):

    try:

        prompt = build_relationship_prompt(
            target_company,
            df
        )

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite offshore wind "
                        "market intelligence strategist."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"ERROR: {str(e)}"