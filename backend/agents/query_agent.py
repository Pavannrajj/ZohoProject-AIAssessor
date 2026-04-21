from asyncio import tasks
from streamlit import context 
from memory.store import last_tasks_store
   


from tools.tools import list_projects, list_tasks,get_task_details,list_project_members,get_task_utilisation

class QueryAgent:
    def handle(self, user_id, message, context):

        message = message.lower()

        
        # ✅ STEP 1: Fetch + store project_id
        if "projects" in message:
            data = list_projects(user_id)

            projects = data.get("projects", [])

            if projects:
                context["project_id"] = projects[0]["id"]   # ✅ store in state
                print("Stored project_id:", context["project_id"])

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
        elif "tasks" in message:
            project_id = context.get("project_id")

            data = list_tasks(user_id, project_id)

            tasks = data.get("tasks", [])

            last_tasks_store[user_id] = tasks
            print("Stored last_tasks:", len(tasks)) 

            return data


        return "I can only fetch data (projects, tasks, etc.)"