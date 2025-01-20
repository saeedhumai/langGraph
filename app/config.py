import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
tavily_api_key = os.getenv("TAVILY_API_KEY")