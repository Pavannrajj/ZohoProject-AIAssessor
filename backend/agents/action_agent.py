from multiprocessing import context
from operator import index
from memory.store import last_tasks_store


from tools.tools import delete_task, create_task, update_task
from memory.store import pending_actions


class ActionAgent:
    def handle(self, user_id, message, context):

        message = message.lower()
        print("LAST TASKS IN ACTION:", context.get("last_tasks"))

        # =========================
        # STEP A: Handle confirmation
        # =========================
        if user_id in pending_actions:

            if message in ["yes", "confirm", "ok", "sure"]:
                action_data = pending_actions.pop(user_id)

                # ✅ DELETE TASK
                if action_data["action"] == "delete_task":

                    project_id = context.get("project_id")

                    if not project_id:
                        return {
                            "requires_confirmation": False,
                            "message": "Please select a project first (use 'show projects')"
                        }

                    result = delete_task(
                        user_id,
                        project_id,
                        action_data["task_id"]
                    )

                    return {
                        "requires_confirmation": False,
                        "message": result
                    }

                # ✅ UPDATE TASK
                elif action_data["action"] == "update_task":

                    project_id = context.get("project_id")

                    if not project_id:
                        return {
                            "requires_confirmation": False,
                            "message": "Please select a project first"
                        }

                    result = update_task(
                        user_id,
                        project_id,
                        action_data["task_id"],
                        action_data["data"]
                    )

                    return {
                        "requires_confirmation": False,
                        "message": "Task updated successfully"
                    }

                # ✅ CREATE TASK (FIXED)
                elif action_data["action"] == "create_task":

                    project_id = context.get("project_id")

                    if not project_id:
                        return {
                            "requires_confirmation": False,
                            "message": "Please select a project first"
                        }

                    result = create_task(
                        user_id,
                        project_id,
                        action_data["task_name"]
                    )

                    return {
                        "requires_confirmation": False,
                        "message": f"Task '{action_data['task_name']}' created successfully"
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

        # =========================
        # STEP B: Create task (WITH CONFIRMATION)
        # =========================
        if "create task" in message:

            project_id = context.get("project_id")

            if not project_id:
                return {
                    "requires_confirmation": False,
                    "message": "Please select a project first (use 'show projects')"
                }

            task_name = message.replace("create task", "").strip()

            if not task_name:
                return {
                    "requires_confirmation": False,
                    "message": "Please provide task name (e.g., create task API integration)"
                }

            pending_actions[user_id] = {
                "action": "create_task",
                "task_name": task_name
            }

            return {
                "requires_confirmation": True,
                "message": f"Create task '{task_name}'?"
            }

        # =========================
        # STEP C: Update task request
        # =========================
        if "update task" in message:

            project_id = context.get("project_id")

            if not project_id:
                return {
                    "requires_confirmation": False,
                    "message": "Please select a project first (use 'show projects')"
                }

            parts = message.split()

            if len(parts) < 4:
                return {
                    "requires_confirmation": False,
                    "message": "Use format: update task <id> <new name>"
                }

            task_id = parts[2]
            new_name = " ".join(parts[3:])

            pending_actions[user_id] = {
                "action": "update_task",
                "task_id": task_id,
                "data": {
                    "name": new_name
                }
            }

            return {
                "requires_confirmation": True,
                "message": f"Update task {task_id} name to '{new_name}'?"
            }

        # =========================
        # STEP D: Delete task
        # =========================
        if "delete task" in message:

            parts = message.split()

            if len(parts) < 3:
                return {
                    "requires_confirmation": False,
                    "message": "Please provide task id (e.g., delete task 5)"
                }

            task_input = parts[-1]
            last_tasks = last_tasks_store.get(user_id, [])
            
            print("LAST TASKS:", last_tasks) 
            if not last_tasks:
                return {
        "requires_confirmation": False,
        "message": "No recent task list found. Please run 'show tasks' first."
    } 
            # ✅ Case 1: User gives number (e.g., delete task 2)
            if task_input.isdigit():

                index = int(task_input) - 1
                print("INDEX:", index, "TOTAL:", len(last_tasks))
                
                if index < 0 or index >= len(last_tasks):
                    return {
            "requires_confirmation": False,
            "message": "Invalid task number"
        }

                task_id = last_tasks[index]["id_string"]

# ✅ Case 2: User gives actual task ID
            else:
                task_id = task_input

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