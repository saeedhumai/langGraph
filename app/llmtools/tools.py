from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
from app.config import tavily_api_key
tavily_client = TavilyClient(api_key=tavily_api_key)
from langchain_community.tools import TavilySearchResults

tool = TavilySearchResults(
    max_results=1,
    include_answer=True,
    include_raw_content=True,
    include_images=False,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)


toolforsearaching ={
            "type": "function",
            "function": {
                "name": "tavily_search",
                "description": "Search the internet for current information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        }


tools = [tool]
# tool.invoke("What's a 'node' in LangGraph?") 
# print(tool.invoke("What is the weather in Dubai ?"))