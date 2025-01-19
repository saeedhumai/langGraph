from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import ChatCompletion
from app.schema.llm.llm import llm
from IPython.display import Image, display
from app.schema.schema import State
# class State(TypedDict):
#     # Messages have the type "list". The `add_messages` function
#     # in the annotation defines how this state key should be updated
#     # (in this case, it appends messages to the list, rather than overwriting them)
#     messages: Annotated[list, add_messages]

from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from openai import ChatCompletion
from app.schema.llm.llm import llm
from IPython.display import Image, display
from app.schema.schema import State
# class State(TypedDict):
#     # Messages have the type "list". The `add_messages` function
#     # in the annotation defines how this state key should be updated
#     # (in this case, it appends messages to the list, rather than overwriting them)
#     messages: Annotated[list, add_messages]

def chatbot(state: State,llm):
   return {"messages": [llm.invoke(state["messages"])]}

def display_graph(graph):
   try:
    display(Image(graph.get_graph().draw_mermaid_png()))
   except Exception:
    # This requires some extra dependencies and is optional
      pass






def main():
   llm = ChatCompletion(model="gpt-4o-mini",api_key=openai_api_key,temperature=0.7)
   # Then add the node
   graph_builder.add_node("chatbot", chatbot(llm))
   # Initialize graph_builder first
   graph_builder = StateGraph(State)
   graph_builder.add_edge(START, "chatbot")
   graph_builder.add_edge("chatbot", END)
   graph = graph_builder.compile()
   input("Press Enter to display the graph...")
   if input == "y":
       display_graph(graph)
   else:
       print("Graph not displayed")
   




if __name__ == "__main__":
    main()



def chatbot(state: State,llm):
   return {"messages": [llm.invoke(state["messages"])]}

def display_graph(graph):
   try:
    display(Image(graph.get_graph().draw_mermaid_png()))
   except Exception:
    # This requires some extra dependencies and is optional
      pass






def main():
   llm = ChatCompletion(model="gpt-4o-mini",api_key=openai_api_key,temperature=0.7)
   # Then add the node
   graph_builder.add_node("chatbot", chatbot(llm))
   # Initialize graph_builder first
   graph_builder = StateGraph(State)
   graph_builder.add_edge(START, "chatbot")
   graph_builder.add_edge("chatbot", END)
   graph = graph_builder.compile()
   input("Press Enter to display the graph...")
   if input == "y":
       display_graph(graph)
   else:
       print("Graph not displayed")
   




if __name__ == "__main__":
    main()
