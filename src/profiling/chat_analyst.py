from openai import OpenAI
from dotenv import load_dotenv

import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================================
# BUILD DATA CONTEXT
# =====================================================

def build_context(df):

    rows = []

    for _, row in df.iterrows():

        rows.append(
            f"""
Company: {row.get("company", "")}
Country: {row.get("country", "")}
Segment: {row.get("segmento", "")}
Strategic Level: {row.get("strategic_level", "")}
Offshore: {row.get("offshore", "")}
Floating: {row.get("floating_wind", "")}
EPC: {row.get("epc", "")}
Digitalization: {row.get("digitalization", "")}
Strategic Score: {row.get("strategic_score", "")}
"""
        )

    return "\n".join(rows[:100])


# =====================================================
# AI ANALYST
# =====================================================

def ask_ai_analyst(question, df):

    try:

        context = build_context(df)

        prompt = f"""
You are an elite offshore wind market intelligence analyst.

Use this companies database to answer the question.

DATABASE:
{context}

QUESTION:
{question}

Provide strategic and concise insights.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior offshore wind "
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