# agents/router.py

from config.llm import llm
from memory.store import pending_actions

def router_node(state):
    message = state["message"].lower()
    user_id = state["user_id"]

    # ✅ STEP 1: Bypass LLM for confirmations (CRITICAL FIX)
    if user_id in pending_actions:
        state["intent"] = "action"
        print("ROUTER: bypass LLM → action")
        return state

    # ✅ STEP 2: Use LLM for normal routing
    prompt = f"""
    Classify the user request:

    Message: "{message}"

    If it is READ (fetch/list/get) → return "query"
    If it is WRITE (create/update/delete/assign) → return "action"

    Only return one word: query OR action
    """

    try:
        result = llm.invoke(prompt).content.strip().lower()
    except Exception as e:
        print("LLM ERROR:", e)

        # ✅ STEP 3: Fallback (VERY IMPORTANT)
        if any(word in message for word in ["create", "delete", "update", "assign"]):
            result = "action"
        else:
            result = "query"

    print("ROUTER INTENT:", result)

    state["intent"] = result
    return state