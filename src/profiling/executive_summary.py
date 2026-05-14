from openai import OpenAI
from dotenv import load_dotenv

import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# BUILD PROMPT
# =====================================================

def build_summary_prompt(row):

    return f"""
You are a senior offshore wind strategy consultant.

Create a concise executive summary for this company.

Include:

1. Company strategic position
2. Offshore wind relevance
3. Innovation assessment
4. Partnership potential
5. Commercial recommendation
6. Risk assessment

COMPANY:
{row.get("company", "")}

COUNTRY:
{row.get("country", "")}

PRODUCT CATEGORY:
{row.get("product_category", "")}

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

WEBSITE:
{row.get("website_text", "")}
"""


# =====================================================
# GENERATE SUMMARY
# =====================================================

def generate_executive_summary(row):

    try:

        prompt = build_summary_prompt(row)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior offshore wind market intelligence expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"ERROR: {str(e)}"