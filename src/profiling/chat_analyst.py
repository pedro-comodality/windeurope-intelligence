from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_ai_analyst(question, df):

    context = df.head(40).to_string()

    prompt = f"""
    You are a senior offshore wind strategic consultant.

    Analyze the following market intelligence data:

    {context}

    User question:
    {question}

    Deliver:
    - strategic insights
    - partnership opportunities
    - acquisition targets
    - ecosystem analysis
    - competitor positioning
    - recommended actions

    Be highly strategic and concise.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content