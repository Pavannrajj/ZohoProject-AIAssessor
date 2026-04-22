from email import message
from multiprocessing import context
from operator import index

from langgraph.func import task
from sympy import preview
from typer import prompt
from memory.store import last_tasks_store

from config.llm import llm
import json


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
# STEP 0: LLM Parsing Layer
# =========================

        prompt = f"""
You are an API action planner.

Message: "{message}"

Extract action details.

Return ONLY valid JSON:

{{
  "action": "create_task | update_task | delete_task | none",
  "task_identifier": "", 
  "task_name": "",
  "data": {{
    "status": "",
    "priority": "",
    "due_date": "",
    "assignee": ""
  }}
}}

Rules:
- task_identifier can be id OR index OR name
- If no action → return action = "none"
- No explanation
- No markdown
"""

        try:
            response = llm.invoke(prompt)
            raw = response.content if hasattr(response, "content") else str(response)
            raw = raw.strip()

            print("ACTION LLM RAW:", raw)

            # ✅ clean markdown
            if raw.startswith("```"):
                raw = raw.replace("```json", "").replace("```", "").strip()

            parsed = json.loads(raw)
            action_type = parsed.get("action")

        except Exception as e:
            print("ACTION LLM ERROR:", e)
            parsed = {"action": "none"}
            

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
        if action_type == "create_task":

            project_id = context.get("project_id")

            if not project_id:
                return {
                    "requires_confirmation": False,
                    "message": "Please select a project first (use 'show projects')"
                }

            task_name = parsed.get("task_name")

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
        elif action_type == "update_task":

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

            task_identifier = parsed.get("task_identifier")
            data = parsed.get("data", {}) # could be ID or name

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

            data = parsed.get("data", {})

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
        elif action_type == "delete_task":

            task_input = parsed.get("task_identifier")
            last_tasks = last_tasks_store.get(user_id, [])

            if not last_tasks:
                return {
            "requires_confirmation": False,
            "message": "No recent task list found. Please run 'show tasks' first."
        }

            task_id = None

    # ✅ Case 1: numeric → could be ID OR index
            if task_input and task_input.isdigit():

        # check if it's a real Zoho ID
                if any(t["id_string"] == task_input for t in last_tasks):
                    task_id = task_input
                else:
            # treat as index
                    index = int(task_input) - 1

                    if index < 0 or index >= len(last_tasks):
                        return {
                    "requires_confirmation": False,
                    "message": "Invalid task number"
                }

                    task_id = last_tasks[index]["id_string"]

    # ✅ Case 2: name match
            else:
                for t in last_tasks:
                    if t["name"].lower() in message.lower():
                        task_id = t["id_string"]
                        break

    # ❌ not found
            if not task_id:
                return {
            "requires_confirmation": False,
            "message": "Task not found"
        }

    # ✅ store pending action
            pending_actions[user_id] = {
        "action": "delete_task",
        "task_id": task_id
    }

            return {
        "requires_confirmation": True,
        "message": f"Are you sure you want to delete task {task_id}?"
    }