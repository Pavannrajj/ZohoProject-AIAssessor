from asyncio import tasks
from email import message
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
class QueryAgent:
    def handle(self, user_id, message, context):

        message = message.lower()

        
        # ✅ STEP 1: Fetch + store project_id
        if "projects" in message:
            data = list_projects(user_id)

            projects = data.get("projects", [])

            if projects:
                context["project_id"] = projects[0]["id_string"]   # ✅ store in state
                print("CURRENT PROJECT:", context.get("project_id"))

            return data
        

        elif "members" in message or "team" in message:

            project_id = context.get("project_id")

            if not project_id:
                return "Please select a project first (use 'show projects')"

            return list_project_members(user_id, project_id)

        elif "utilisation" in message or "utilization" in message:

            project_id = context.get("project_id")

            if not project_id:
                return "Please select a project first (use 'show projects')"

            return get_task_utilisation(user_id, project_id)
        
        elif "task details" in message or "details" in message:
            project_id = context.get("project_id")

            if not project_id:
                return "Please select a project first (use 'show projects')"

            parts = message.split()

            if len(parts) < 3:
                return "Please provide task id (e.g., task details 5)"

            task_id = parts[-1]

            return get_task_details(user_id, project_id, task_id)

        # ✅ STEP 2: Use stored project_id
        if "task" in message:

            project_id = context.get("project_id")

            if not project_id:
                return {"message": "Please select a project first"}

            filters = extract_filters(message)

            result = list_tasks(user_id, project_id, filters)

    # ✅ IMPORTANT: store tasks for delete/update by index
            last_tasks_store[user_id] = result.get("tasks", [])

            print("STORED TASKS:", last_tasks_store[user_id])  # debug

            return result