from tools.tools import delete_task,create_task
from memory.store import pending_actions

class ActionAgent:
    def handle(self, user_id, message, context):

        message = message.lower()

        # STEP A: Handle confirmation
        if user_id in pending_actions:

            if message in ["yes", "confirm", "ok", "sure"]:
                action_data = pending_actions.pop(user_id)

                if action_data["action"] == "delete_task":

                    project_id = context.get("project_id")

                    if not project_id:
                        return {
                            "requires_confirmation": False,
                            "message": "Please select a project first (use 'show projects')"
                        }
                    print("PROJECT ID:", project_id)
                    print("TASK ID:", action_data["task_id"])
                    result = delete_task(
                        user_id,
                        project_id,
                        action_data["task_id"]
                    )

                    return {
                        "requires_confirmation": False,
                        "message": result
                    }

            elif message in ["no", "cancel"]:
                pending_actions.pop(user_id)
                return {
                    "requires_confirmation": False,
                    "message": "Action cancelled"
                }

            else:
                return {
                    "requires_confirmation": True,
                    "message": "Please confirm with yes or no"
                }
        # STEP B: Create task
        if "create task" in message:

            project_id = context.get("project_id")

            if not project_id:
                return {
                    "requires_confirmation": False,
                    "message": "Please select a project first (use 'show projects')"
                    }

                

            # extract task name
            task_name = message.replace("create task", "").strip()

            if not task_name:
                return {
                    "requires_confirmation": False,
                    "message": "Please provide task name (e.g., create task API integration)"
                }

            result = create_task(user_id, project_id, task_name)

            return {
                "requires_confirmation": False,
                "message": result
            }
        # STEP B: New delete request
        if "delete task" in message:
            parts = message.split()

            if len(parts) < 3:
                return {
                    "requires_confirmation": False,
                    "message": "Please provide task id (e.g., delete task 5)"
                }

            task_id = parts[-1]

            pending_actions[user_id] = {
                "action": "delete_task",
                "task_id": task_id
            }

            return {
                "requires_confirmation": True,
                "message": f"Are you sure you want to delete task {task_id}?"
            }

        return {
            "requires_confirmation": False,
            "message": "I handle create/update/delete operations only"
        }