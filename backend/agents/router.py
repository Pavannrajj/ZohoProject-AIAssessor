from models.state import GraphState
from config.llm import llm
from memory.store import pending_actions
import json


def router_node(state: GraphState):
    message = state["message"].lower()
    user_id = state["user_id"]

    # ✅ Always respect pending action
    if user_id in pending_actions:
        state["intent"] = "action"
        print("ROUTER: bypass → action")
        return state

    prompt = f"""
You are an intent classifier.

Message: "{message}"

Classify into ONE:

QUERY → reading data
Examples:
- show projects
- list tasks
- task details
- who is assigned
- utilisation

ACTION → modifying data
Examples:
- create task
- update task
- delete task
- assign task

Rules:
- "details", "show", "list", "get" → ALWAYS query
- "create", "update", "delete", "assign" → ALWAYS action

Return ONLY JSON:
{{"intent": "query"}} OR {{"intent": "action"}}
"""

    try:
        response = llm.invoke(prompt)

        raw = response.content if hasattr(response, "content") else str(response)
        raw = raw.strip()

        print("LLM RAW:", raw)

        # ✅ FIX: clean markdown
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        if not raw:
            raise ValueError("Empty LLM response")

        parsed = json.loads(raw)

        state["intent"] = parsed["intent"]

        print("ROUTER LLM:", state["intent"])
        return state

    except Exception as e:
        print("ROUTER FAILURE:", e)
        return state   