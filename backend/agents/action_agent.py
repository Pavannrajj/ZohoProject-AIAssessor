from email import message
from multiprocessing import context
from operator import index

from langgraph.func import task
from sympy import preview
from memory.store import last_tasks_store


from tools.tools import delete_task, create_task, find_task_by_name, update_task
from memory.store import pending_actions

import re

def extract_update_fields(message: str):
    data = {}

    # name
    name_match = re.search(r"name (.+?)(?= status| priority| due|$)", message)
    if name_match:
        data["name"] = name_match.group(1).strip()

    # status
    status_match = re.search(r"status (open|closed|in progress|on hold)", message)
    if status_match:
        data["status"] = status_match.group(1)

    # priority
    priority_match = re.search(r"priority (high|medium|low)", message)
    if priority_match:
        data["priority"] = priority_match.group(1)

    # due date
    due_match = re.search(r"due (\d{4}-\d{2}-\d{2})", message)
    if due_match:
        data["due_date"] = due_match.group(1)

    # assignee
    assign_match = re.search(r"assign to (\w+)", message)
    if assign_match:
        data["assignee"] = assign_match.group(1)

    return data


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

            if len(parts) < 3:
                return {
        "requires_confirmation": False,
        "message": "Use format: update task <id> ..."
    }

            keywords = ["name", "status", "priority", "due"]

            task_name_parts = []
            for word in parts[2:]:
                if word in keywords:
                    break
                task_name_parts.append(word)

            task_identifier = " ".join(task_name_parts)  # could be ID or name

            project_id = context.get("project_id")

# ✅ Check if numeric → treat as ID
            if task_identifier.isdigit():

                last_tasks = last_tasks_store.get(user_id, [])

                if not last_tasks:
                    return {
            "requires_confirmation": False,
            "message": "No recent task list found. Please run 'show tasks' first."
        }

                index = int(task_identifier) - 1

                if index < 0 or index >= len(last_tasks):
                    return {
            "requires_confirmation": False,
            "message": "Invalid task number"
        }

                task_id = last_tasks[index]["id_string"]

            else:
                task = find_task_by_name(user_id, project_id, task_identifier)

                if not task:
                    return {
            "requires_confirmation": False,
            "message": f"Task '{task_identifier}' not found"
        }

                task_id = task["id_string"]

            data = extract_update_fields(message)

            if not data:
                return {
        "requires_confirmation": False,
        "message": "Please provide fields (name/status/priority/due date)"
    }

            pending_actions[user_id] = {
    "action": "update_task",
    "task_id": task_id,
    "data": data
}

            preview = "\n".join([f"- {k}: {v}" for k, v in data.items()])

            return {
    "requires_confirmation": True,
    "message": f"Update Task {task_id}:\n{preview}\nConfirm? (yes/no)"
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