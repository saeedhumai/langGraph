import sys
sys.dont_write_bytecode = True
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from app.llm.llmconfig import llm
from app.schema.schema import State
from IPython.display import Image, display
import os

def chatbot(state: State, llm_func):
    # Convert messages to the format OpenAI expects
    messages = []
    for msg in state["messages"]:
        if hasattr(msg, "content"):
            role = "user" if "Human" in msg.__class__.__name__ else "assistant"
            messages.append({"role": role, "content": msg.content})
        else:
            # Handle dictionary format
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg["content"]
            })
    
    response = llm_func(messages)
    return {"messages": [{"role": "assistant", "content": response.content}]}

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

def stream_graph_updates(graph, user_input: str):
    # Format initial message with proper role
    initial_messages = [{"role": "user", "content": user_input}]
    
    for event in graph.stream({"messages": initial_messages}):
        for value in event.values():
            message = value["messages"][-1]
            content = message["content"] if isinstance(message, dict) else message.content
            print("Assistant:", content)
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(graph, user_input)
        except Exception as e:
            print(f"Error: {str(e)}")
            break

def main():  
   graph = create_graph()
   user_input = input("User: ")
   stream_graph_updates(graph , user_input)
   save_graph(graph)
   

if __name__ == "__main__":
    main()
