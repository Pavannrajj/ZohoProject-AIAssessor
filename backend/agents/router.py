from models.state import GraphState
from config.llm import llm
from memory.store import pending_actions


def router_node(state: GraphState):
    message = state["message"].lower()
    user_id = state["user_id"]

    # STEP 1: Bypass LLM for confirmations
    if user_id in pending_actions:
        state["intent"] = "action"
        print("ROUTER: bypass LLM → action")
        return state

    # STEP 2: LLM routing
    prompt = f"""
    Classify the user request:

    Message: "{message}"

    If it is READ (fetch/list/get/details) → return "query"
    If it is WRITE (create/update/delete/assign) → return "action"

    Only return one word: query OR action
    """

    try:
        result = llm.invoke(prompt).content.strip().lower()
    except Exception as e:
        print("LLM ERROR:", e)

        # ✅ Fallback routing
        if any(word in message for word in [
            "show", "list", "get", "tasks", "projects", "members", "utilisation", "utilization"
        ]):
            state["intent"] = "query"
        else:
            state["intent"] = "action"

        print("ROUTER: fallback →", state["intent"])
        return state

    state["intent"] = result
    return state