from agents.action_agent import ActionAgent

agent = ActionAgent()

def action_node(state):
    result = agent.handle(
        message=state["message"],
        user_id=state["user_id"],
        context=state
    )

    # Always dict now
    if result.get("requires_confirmation"):
        state["pending_action"] = result
        state["response"] = result["message"]
        return state

    state["pending_action"] = None
    state["response"] = result.get("message")
    return state