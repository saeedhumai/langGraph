from openai import ChatCompletion

llm = ChatCompletion(model="gpt-4o-mini",api_key=openai_api_key,temperature=0.7)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)