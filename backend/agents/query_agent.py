from email.mime import message

from memory.store import last_tasks_store
from memory.store import last_projects_store
from memory.memory import save_memory, get_memory

from tools.tools import find_project_by_name, list_projects, list_tasks,get_task_details,list_project_members,get_task_utilisation

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
        message = message.lower()
        # ✅ FETCH MEMORY
        if any(q in message for q in [
    "important project",
    "which project is important",
    "what is my important project"
]):
            project = get_memory(user_id, "important_project")

            if project:
                return {"message": f"Your important project is {project}"}
            else:
                return {"message": "You haven't set any important project yet."}


        # ✅ SAVE MEMORY
        if "important" in message and "is" in message:

            projects = last_projects_store.get(user_id)

    # 🔥 fallback to API (VERY IMPORTANT)
            if not projects:
                data = list_projects(user_id)
                projects = data.get("projects", [])
                last_projects_store[user_id] = projects

            clean_msg = message.lower().replace("-", " ")

            matched = False

            for p in projects:
                project_name = p["name"].lower().replace("-", " ")

                if project_name in clean_msg:
                    save_memory(user_id, "important_project", p["name"])
                    matched = True
                    return {"message": f"Got it. I'll remember {p['name']} as important."}   

            if not matched:
                    return {"message": "Please mention a valid project name."}
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
- select_project

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
            last_projects_store[user_id] = projects

            return data

        # ❗ All below need project_id
        elif operation == "select_project":

            projects = last_projects_store.get(user_id, [])

            if not projects:
                return {"message": "Please run 'show projects' first"}

            project_input = message.lower()

            project_id = None

    # ✅ Case 1: extract number (e.g. "select project 1")
            import re
            num_match = re.search(r"\d+", project_input)

            if num_match:
                index = int(num_match.group()) - 1
                if 0 <= index < len(projects):
                    project_id = projects[index]["id_string"]

    # ✅ Case 2: extract name (e.g. "select project first-project")
            if not project_id:
                name_match = re.search(r"select project (.+)", project_input)

                if name_match:
                    name = name_match.group(1).strip()
                else:
                    name = project_input.strip()

                project = find_project_by_name(user_id, name)

                if project:
                    project_id = project["id_string"]

            if not project_id:
                return {"message": "Project not found"}

            context["project_id"] = project_id

            return {"message": f"Project selected successfully"}

            projects = last_projects_store.get(user_id, [])

            project_input = message.strip().lower()

            project_id = None

# ✅ index
            if project_input.isdigit():
                index = int(project_input) - 1
                if 0 <= index < len(projects):
                    project_id = projects[index]["id_string"]

# ✅ name
            else:
                project = find_project_by_name(user_id, project_input)
                if project:
                    project_id = project["id_string"]

            if not project_id:
                return {"message": "Project not found"}

            context["project_id"] = project_id

            return {"message": "Project selected successfully"}

            projects = last_projects_store.get(user_id, [])

            project_input = message.strip().lower()

            project_id = None

    # ✅ index
            if project_input.isdigit():
                index = int(project_input) - 1
                if 0 <= index < len(projects):
                    project_id = projects[index]["id_string"]

    # ✅ name
            else:
                project = find_project_by_name(user_id, project_input)
                if project:
                    project_id = project["id_string"]

            if not project_id:
                return {"message": "Project not found"}

            context["project_id"] = project_id

            return {"message": "Project selected successfully"}
        
        if not context.get("project_id"):
            return {"message": "Please select a project first (use 'show projects')"}

        # ✅ 2. LIST TASKS
        if operation == "list_tasks":
            filters = parsed.get("filters", {})

            result = list_tasks(user_id, context.get("project_id"), filters)

            # store for later delete/update
            last_tasks_store[user_id] = result.get("tasks", [])
            print("STORED TASKS:", last_tasks_store[user_id])

            return result

        # ✅ 3. TASK DETAILS
        elif operation == "get_task_details":
            task_input = parsed.get("task_id")
            tasks = last_tasks_store.get(user_id, [])

            if not tasks:
                return {"message": "Please run 'show tasks' first."}

            task_id = None

    # ✅ Case 1: numeric → ID or index
            if task_input and task_input.isdigit():

        # real Zoho ID
                if any(t["id_string"] == task_input for t in tasks):
                    task_id = task_input
                else:
                    index = int(task_input) - 1

                    if index < 0 or index >= len(tasks):
                        return {"message": "Invalid task number"}

                    task_id = tasks[index]["id_string"]

    # ✅ Case 2: name → match
            else:
                for t in tasks:
                    if t["name"].lower() == task_input.lower():
                        task_id = t["id_string"]
                        break

        # fallback partial match
                if not task_id:
                    for t in tasks:
                        if task_input.lower() in t["name"].lower():
                            task_id = t["id_string"]
                            break

    # ❌ still not found
            if not task_id:
                return {"message": "Task not found. Use task number or exact name."}

    # ✅ FINAL CALL (ONLY with valid ID)
            return get_task_details(user_id,context.get("project_id"), task_id)
  # ✅ 4. MEMBERS
        elif operation == "list_members":
            return list_project_members(user_id,context.get("project_id"))

        # ✅ 5. UTILISATION
        elif operation == "utilisation":
            return get_task_utilisation(user_id, context.get("project_id"))


        # ❌ Unknown
        return {"message": "Unknown query operation"}
    
