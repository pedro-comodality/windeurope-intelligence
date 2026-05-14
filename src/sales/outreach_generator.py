from openai import OpenAI
from dotenv import load_dotenv

import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# GENERATE OUTREACH EMAIL
# =====================================================

def generate_outreach_email(row):

    try:

        prompt = f"""
You are a senior offshore wind business developer.

Create a professional outreach email.

COMPANY:
{row.get("company", "")}

COUNTRY:
{row.get("country", "")}

SEGMENT:
{row.get("segmento", "")}

STRATEGIC LEVEL:
{row.get("strategic_level", "")}

OFFSHORE:
{row.get("offshore", "")}

FLOATING WIND:
{row.get("floating_wind", "")}

EPC:
{row.get("epc", "")}

WEBSITE INFO:
{row.get("website_text", "")}

Requirements:
- concise
- professional
- strategic
- partnership-oriented
- offshore wind industry tone
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior offshore wind "
                        "sales strategist."
                    )
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