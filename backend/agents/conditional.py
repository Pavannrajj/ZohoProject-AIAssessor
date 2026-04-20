# agents/conditional.py

def route_decision(state):
    if state["intent"] == "query":
        return "query_node"
    else:
        return "action_node"