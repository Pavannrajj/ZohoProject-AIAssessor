from asyncio import tasks
from email import message
from operator import index
from operator import index
from urllib import response
from streamlit import context 
from memory.store import last_tasks_store
   


from tools.tools import list_projects, list_tasks,get_task_details,list_project_members,get_task_utilisation

import re

def extract_filters(message: str):
    filters = {}

    message = message.lower()

    # ✅ Normalize user → Zoho status
    if "completed" in message or "closed" in message:
        filters["status"] = "closed"

    elif "open" in message:
        filters["status"] = "open"

    elif "in progress" in message:
        filters["status"] = "in progress"

    elif "on hold" in message:
        filters["status"] = "on hold"

    # assignee
    assignee_match = re.search(r"assigned to (\w+)", message)
    if assignee_match:
        filters["assignee"] = assignee_match.group(1)

    return filters
from tools.tools import (
    list_projects,
    list_tasks,
    get_task_details,
    list_project_members,
    get_task_utilisation
)
from memory.store import last_tasks_store
from config.llm import llm
import json


class QueryAgent:
    def handle(self, user_id, message, context):

        project_id = context.get("project_id")

        # 🔷 LLM Prompt
        prompt = f"""
You are an API planner.

Message: "{message}"

You MUST choose ONE operation from this list EXACTLY:

- list_projects
- list_tasks
- get_task_details
- list_members
- utilisation

Return ONLY valid JSON:

{{
  "operation": "one_of_above",
  "task_id": "",
  "filters": {{
    "status": "",
    "assignee": ""
  }}
}}

Rules:
- Do NOT invent new operation names
- Do NOT use synonyms like "get_tasks"
- Only use the exact values provided
- No explanation
- No markdown
"""

        try:
            response = llm.invoke(prompt)

            raw = response.content if hasattr(response, "content") else str(response)
            raw = raw.strip()

            print("QUERY LLM RAW:", raw)

# ✅ FIX HERE
            if raw.startswith("```"):
                raw = raw.replace("```json", "").replace("```", "").strip()

            if not raw:
                raise ValueError("Empty LLM response")

            parsed = json.loads(raw)

        except Exception as e:
            print("QUERY LLM ERROR:", e)
            return {"message": "Sorry, I couldn’t understand that. Please rephrase."}

        operation = parsed.get("operation")

        # =============================
        # EXECUTION LAYER (NO LLM HERE)
        # =============================

        # ✅ 1. LIST PROJECTS
        if operation == "list_projects":
            data = list_projects(user_id)

            projects = data.get("projects", [])
            if projects:
                context["project_id"] = projects[0]["id_string"]
                print("CURRENT PROJECT:", context["project_id"])

            return data

        # ❗ All below need project_id
        if not project_id:
            return {"message": "Please select a project first (use 'show projects')"}

        # ✅ 2. LIST TASKS
        if operation == "list_tasks":
            filters = parsed.get("filters", {})

            result = list_tasks(user_id, project_id, filters)

            # store for later delete/update
            last_tasks_store[user_id] = result.get("tasks", [])
            print("STORED TASKS:", last_tasks_store[user_id])

            return result

        # ✅ 3. TASK DETAILS
        elif operation == "get_task_details":
            task_id = parsed.get("task_id")
            tasks = last_tasks_store.get(user_id, [])

    # ✅ Case 1: If numeric → could be index OR real ID
            if task_id and task_id.isdigit():

        # If matches a real Zoho ID → use directly
                    if any(t["id_string"] == task_id for t in tasks):
                        pass
                    else:
            # treat as index
                        index = int(task_id) - 1

                        if index < 0 or index >= len(tasks):
                            return {"message": "Invalid task number"}

                        task_id = tasks[index]["id_string"]

    # ✅ Case 2: If empty → match by name
            if not task_id:
                msg = message.lower().strip()

                for t in tasks:
                    task_name = t["name"].lower().strip()

        # exact match
                    if msg.endswith(task_name):
                        task_id = t["id_string"]
                        break

        # partial match (fallback)
                    if task_name in msg:
                        task_id = t["id_string"]
                        break

    # ✅ Case 3: still not found
            if not task_id:
                return {"message": "Task not found. Use task number or exact name."}

    # ✅ FINAL FIX (you missed this)
            return get_task_details(user_id, project_id, task_id)
        # ✅ 4. MEMBERS
        elif operation == "list_members":
            return list_project_members(user_id, project_id)

        # ✅ 5. UTILISATION
        elif operation == "utilisation":
            return get_task_utilisation(user_id, project_id)

        # ❌ Unknown
        return {"message": "Unknown query operation"}