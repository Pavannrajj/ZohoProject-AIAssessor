# agents/router.py

from config.llm import llm

def router_node(state):
    message = state["message"]

    prompt = f"""
    Classify the user request:

    Message: "{message}"

    If it is READ (fetch/list/get) → return "query"
    If it is WRITE (create/update/delete/assign) → return "action"

    Only return one word: query OR action
    """

    result = llm.invoke(prompt).content.strip().lower()

    state["intent"] = result
    return state