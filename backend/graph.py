# graph.py

from langgraph.graph import StateGraph, END

from models.state import GraphState
from agents.router import router_node
from agents.query_node import query_node
from agents.action_node import action_node
from agents.conditional import route_decision

builder = StateGraph(GraphState)

# nodes
builder.add_node("router", router_node)
builder.add_node("query_node", query_node)
builder.add_node("action_node", action_node)

# flow
builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "query_node": "query_node",
        "action_node": "action_node"
    }
)

builder.add_edge("query_node", END)
builder.add_edge("action_node", END)

graph = builder.compile()