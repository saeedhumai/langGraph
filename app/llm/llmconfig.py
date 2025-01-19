from openai import OpenAI
from app.config import openai_api_key

client = OpenAI(api_key=openai_api_key)

def llm(messages):
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message


