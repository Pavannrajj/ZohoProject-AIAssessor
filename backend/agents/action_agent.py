from tools.tools import delete_task
from memory.store import pending_actions

class ActionAgent:
    def handle(self, user_id, message, context):

        message = message.lower()

        # STEP A: Check confirmation
        if user_id in pending_actions:

            if message in ["yes", "confirm", "ok", "sure"]:
                action_data = pending_actions.pop(user_id)

                if action_data["action"] == "delete_task":
                    
                    project_id = context.get("project_id")   # ✅ get project

                    if not project_id:
                        return "Please select a project first (use 'show projects')"

                    return delete_task(
                        user_id,
                        project_id,
                        action_data["task_id"]   # ✅ pass both
                    )

            elif message in ["no", "cancel"]:
                pending_actions.pop(user_id)
                return "Action cancelled"

            else:
                return "Please confirm with yes or no"

        # STEP B: New request
        if "delete task" in message:
            parts = message.split()

            if len(parts) < 3:
                return "Please provide task id (e.g., delete task 5)"

            task_id = parts[-1]

            pending_actions[user_id] = {
                "action": "delete_task",
                "task_id": task_id
            }

            return f"Are you sure you want to delete task {task_id}?"

        return "I handle create/update/delete operations only"