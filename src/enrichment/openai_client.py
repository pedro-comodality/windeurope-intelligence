import json
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def build_prompt(row):

    return f"""
You are a senior offshore wind industry analyst.

Analyze this WindEurope exhibitor.

Company: {row['company']}

Country: {row['country']}

Website: {row['website']}

Generation Type:
{row['generation_type']}

Product Category:
{row['product_category']}

Return ONLY valid JSON.

Required schema:

{{
    "segmento": "",
    "nivel_tecnologico": 0,
    "potencial_offshore": 0,
    "potencial_floating": 0,
    "potencial_epc": 0,
    "supply_chain": 0,
    "partner_estrategico": 0,
    "innovacion": 0,
    "crecimiento": 0,
    "tipo_empresa": "",
    "ia": false,
    "digitalizacion": false,
    "robotics": false,
    "predictive_maintenance": false,
    "cable_systems": false,
    "foundations": false,
    "maritime_logistics": false,
    "floating_wind": false
}}

Scoring:
0-10 only.
Be conservative.
Focus on offshore wind.
Focus on floating wind.
Focus on EPC and industrial value.
"""


def analyze_company(row):

    prompt = build_prompt(row)

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        temperature=0.1,

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)