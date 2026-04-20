from tools.tools import list_projects, list_tasks

class QueryAgent:
    def handle(self, user_id, message, context):

        message = message.lower()

        # ✅ STEP 8 — STORE project_id
        if "projects" in message:
            data = list_projects(user_id)

            projects = data.get("projects", [])

            if projects:
                context["project_id"] = projects[0]["id"]   # ✅ store
                print("Stored project_id:", context["project_id"])  # debug

            return data

        # ✅ USE stored project_id
        elif "tasks" in message:
            project_id = context.get("project_id")

            if not project_id:
                return "Please select a project first (use 'show projects')"

            return list_tasks(user_id, project_id)
            

        return "I can only fetch data (projects, tasks, etc.)"