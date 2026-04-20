from agents.query_agent import QueryAgent

agent = QueryAgent()

def query_node(state):
    response = agent.handle(
        user_id=state["user_id"],
        message=state["message"],
        context=state   # 🔥 THIS is your memory
    )

    state["response"] = response
    return state