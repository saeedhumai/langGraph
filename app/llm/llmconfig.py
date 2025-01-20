from openai import OpenAI
from app.config import openai_api_key
from app.llmtools.tools import toolforsearaching
client = OpenAI(api_key=openai_api_key)

    
def llm(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        tools=[toolforsearaching]
    )
    return response.choices[0].message

