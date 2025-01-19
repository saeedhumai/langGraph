from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import ChatCompletion

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def chatbot(state: State,llm):
   return {"messages": [llm.invoke(state["messages"])]}



# Then add the node




def main():
   llm = ChatCompletion(model="gpt-4o-mini",api_key=openai_api_key,temperature=0.7)
   graph_builder.add_node("chatbot", chatbot(llm))
   # Initialize graph_builder first
   graph_builder = StateGraph(State)

   # print(f"openai_api_key is loaded : {openai_api_key}")
   # print(f"graph_builder is loaded : {graph_builder}")
   



if __name__ == "__main__":
    main()
