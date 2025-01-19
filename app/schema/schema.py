from typing import Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    # Messages have the type "list[dict]". The `add_messages` function
    # in the annotation defines how this state key should be updated
    messages: Annotated[list[dict], add_messages]


