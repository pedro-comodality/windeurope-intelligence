from openai import OpenAI
from dotenv import load_dotenv

import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# MEETING PREPARATION
# =====================================================

def generate_meeting_prep(row):

    try:

        prompt = f"""
You are a senior offshore wind business strategist.

Prepare a strategic meeting briefing.

COMPANY:
{row.get("company", "")}

COUNTRY:
{row.get("country", "")}

SEGMENT:
{row.get("segmento", "")}

STRATEGIC LEVEL:
{row.get("strategic_level", "")}

LEAD SCORE:
{row.get("lead_score", "")}

STRATEGIC SCORE:
{row.get("strategic_score", "")}

OFFSHORE:
{row.get("offshore", "")}

FLOATING WIND:
{row.get("floating_wind", "")}

EPC:
{row.get("epc", "")}

WEBSITE INFO:
{row.get("website_text", "")}

Create:
- executive briefing
- key opportunities
- partnership strategy
- negotiation approach
- meeting objectives
- business risks
- strategic recommendations
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an elite offshore wind "
                        "strategy consultant."
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