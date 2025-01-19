import sys
sys.dont_write_bytecode = True
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from app.llm.llmconfig import llm
from app.schema.schema import State
from IPython.display import Image, display
import os
def chatbot(state: State, llm):
   return {"messages": [llm.invoke(state["messages"])]}

def save_graph(graph):
    try:
        # Create graphs directory if it doesn't exist
        os.makedirs('graphs', exist_ok=True)
        
        # Get the binary data
        png_data = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        filepath = os.path.join('graphs', 'graph.png')
        with open(filepath, 'wb') as f:
            f.write(bytes(png_data))
        print(f"Graph saved to: {filepath}")
    except Exception as e:
        print(f"Error saving graph: {str(e)}")

def create_graph():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", lambda state: chatbot(state, llm))
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    return graph_builder.compile()


def main():  
   graph = create_graph()

   save_graph(graph)

if __name__ == "__main__":
    main()
