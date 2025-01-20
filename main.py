import sys
import logging
sys.dont_write_bytecode = True
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from app.llm.llmconfig import llm
from app.schema.schema import State
from IPython.display import Image, display
import os
import json
from fastapi import FastAPI

app = FastAPI()

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def chatbot(state: State, llm_func):
    messages = []
    logger.debug(f"Incoming state: {state}")
    
    for msg in state["messages"]:
        if hasattr(msg, "content"):
            role = "user" if "Human" in msg.__class__.__name__ else "assistant"
            messages.append({"role": role, "content": msg.content})
        else:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg["content"]
            })
    
    logger.debug(f"Processed messages: {messages}")
    
    try:
        response = llm_func(messages)
        logger.debug(f"LLM Response: {response}")
        
        # Check for tool_calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            logger.info(f"Tool calls detected: {response.tool_calls}")
            from app.llmtools.tools import tool
            
            tool_call = response.tool_calls[0]
            # Parse the arguments string into a dictionary
            arguments = json.loads(tool_call.function.arguments)
            search_query = arguments.get("query")
            logger.debug(f"Search query: {search_query}")
            
            try:
                search_result = tool.invoke(search_query)
                logger.debug(f"Search result: {search_result}")
                
                # Add the tool call result to messages
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {"name": "tavily_search", "arguments": tool_call.function.arguments}
                    }]
                })
                
                messages.append({
                    "role": "tool",
                    "content": str(search_result),
                    "tool_call_id": tool_call.id,
                    "name": "tavily_search"
                })
                
                # Get final response from LLM with search results
                final_response = llm_func(messages)
                logger.debug(f"Final response with search results: {final_response}")
                
                if hasattr(final_response, 'content'):
                    return {"messages": [{"role": "assistant", "content": final_response.content}]}
                else:
                    return {"messages": [{"role": "assistant", "content": str(final_response)}]}
                
            except Exception as e:
                logger.error(f"Error during search: {str(e)}", exc_info=True)
                return {"messages": [{"role": "assistant", "content": f"I encountered an error while searching: {str(e)}"}]}
        
        # Handle direct responses
        if hasattr(response, 'content') and response.content is not None:
            return {"messages": [{"role": "assistant", "content": response.content}]}
        else:
            return {"messages": [{"role": "assistant", "content": "I'm searching for that information..."}]}
            
    except Exception as e:
        logger.error(f"Error in chatbot function: {str(e)}", exc_info=True)
        return {"messages": [{"role": "assistant", "content": f"Error: {str(e)}"}]}

def save_graph(graph):
    try:
        os.makedirs('graphs', exist_ok=True)
        png_data = graph.get_graph().draw_mermaid_png()
        filepath = os.path.join('graphs', 'graph.png')
        with open(filepath, 'wb') as f:
            f.write(bytes(png_data))
        logger.info(f"Graph saved to: {filepath}")
    except Exception as e:
        logger.error(f"Error saving graph: {str(e)}", exc_info=True)

def create_graph():
    try:
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", lambda state: chatbot(state, llm))
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        logger.info("Graph created successfully")
        return graph_builder.compile()
    except Exception as e:
        logger.error(f"Error creating graph: {str(e)}", exc_info=True)
        raise

def stream_graph_updates(graph, user_input: str):
    logger.debug(f"Processing user input: {user_input}")
    initial_messages = [{"role": "user", "content": user_input}]
    
    try:
        for event in graph.stream({"messages": initial_messages}):
            for value in event.values():
                message = value["messages"][-1]
                content = message["content"] if isinstance(message, dict) else message.content
                print("Assistant:", content)
                logger.debug(f"Assistant response: {content}")
    except Exception as e:
        logger.error(f"Error in stream processing: {str(e)}", exc_info=True)

def main():
    try:
        logger.info("Starting application")
        graph = create_graph()
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    logger.info("User requested to exit")
                    print("Goodbye!")
                    break
                
                stream_graph_updates(graph, user_input)
                save_graph(graph)
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}", exc_info=True)
                break

    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}", exc_info=True)

@app.get("/askquestion")
def askquestion(question: str):
    try:
        graph = create_graph()
        initial_messages = [{"role": "user", "content": question}]
        responses = []
        
        for event in graph.stream({"messages": initial_messages}):
            for value in event.values():
                message = value["messages"][-1]
                content = message["content"] if isinstance(message, dict) else message.content
                responses.append(content)
        
        return {"response": responses[-1] if responses else "No response generated"}
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        return {"error": str(e)}

@app.get("/schema")
def schema():
    schema = State.messages
    return {"messages": schema}

if __name__ == "__main__":
    main()


