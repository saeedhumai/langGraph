
from app.config import openai_api_key
from openai import ChatCompletion


llm = ChatCompletion(
    model="gpt-4o-mini",
    api_key=openai_api_key,
    temperature=0.7
)


