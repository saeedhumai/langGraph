import sys
sys.dont_write_bytecode = True
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from app.llm.llmconfig import llm
from app.schema.schema import State
from IPython.display import Image, display

def chatbot(state: State, llm):
   return {"messages": [llm.invoke(state["messages"])]}

def display_graph(graph):
   try:
    display(Image(graph.get_graph().draw_mermaid_png()))
   except Exception:
    # This requires some extra dependencies and is optional
      print("Could not display graph - missing dependencies")
      pass

def main():
   # Initialize graph_builder
   graph_builder = StateGraph(State)
   # Add the node with lambda
   graph_builder.add_node("chatbot", lambda state: chatbot(state, llm))
   graph_builder.add_edge(START, "chatbot")
   graph_builder.add_edge("chatbot", END)
   graph = graph_builder.compile()
   
   user_input = input("Press Enter to display the graph, or any other key to skip: ")
   if user_input.strip() == "":
       display_graph(graph)
       for w in graph.get_graph().draw_mermaid_png():
           print(w)
   else:
       print("Graph not displayed")

if __name__ == "__main__":
    main()
