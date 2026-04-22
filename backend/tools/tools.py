from asyncio import tasks

from .zoho_client import ZohoClient

def list_projects(user_id):
    client = ZohoClient(user_id)
    return client.get_projects()

def list_tasks(user_id, project_id, filters=None):
    client = ZohoClient(user_id=user_id)

    tasks = client.get_tasks(project_id)

    if not filters:
        return {"tasks": tasks}

    filtered_tasks = tasks

    # ✅ Filter by status
    if filters.get("status"):

        filtered_tasks = [
            t for t in filtered_tasks
            if filters["status"] in (t.get("status", {}).get("name", "") or "").lower()
        ]

    # ✅ Filter by assignee
    if filters.get("assignee"):
        filtered_tasks = [
        t for t in filtered_tasks
        if any(
            filters["assignee"].lower() in (owner.get("name", "").lower())
            for owner in t.get("details", {}).get("owners", [])
        )
    ]

    # ✅ Filter by due date
    if filters.get("due_date"):
        filtered_tasks = [
            t for t in filtered_tasks
            if (t.get("due_date") or "") == filters["due_date"]
        ]
        print("FILTERS:", filters)
        print("TOTAL TASKS:", len(tasks))
        print("FILTERED:", len(filtered_tasks))

    return {"tasks": filtered_tasks}

def create_task(user_id, project_id, name):
    client = ZohoClient(user_id)
    return client.create_task(project_id, name)

def delete_task(user_id, project_id, task_id):
    client = ZohoClient(user_id)
    return client.delete_task(project_id, task_id)

def get_task_details(user_id, project_id, task_id):
    client = ZohoClient(user_id)
    return client.get_task_details(project_id, task_id)

def update_task(user_id, project_id, task_id, data):
    client = ZohoClient(user_id)

    payload = {}

    # ✅ Map fields safely
    if "name" in data:
        payload["name"] = data["name"]

    if "status" in data:
        payload["status"] = data["status"]

    if "priority" in data:
        payload["priority"] = data["priority"]

    if "due_date" in data:
        payload["due_date"] = data["due_date"]

    if "assignee" in data:
        payload["owner"] = data["assignee"]  # Zoho may expect user ID later

    return client.update_task(project_id, task_id, payload)

def list_project_members(user_id, project_id):
    client = ZohoClient(user_id)
    return client.get_project_members(project_id)


def get_task_utilisation(user_id, project_id):
    from tools.tools import list_tasks  # reuse existing

    tasks = list_tasks(user_id, project_id)

    summary = {}

    for task in tasks.get("tasks", []):
        owners = task.get("details", {}).get("owners", [])

        if owners and isinstance(owners, list):
            owner = owners[0].get("name", "Unknown")
        else:
            owner = "Unknown"
            
        summary[owner] = summary.get(owner, 0) + 1

    return summary


def find_task_by_name(user_id, project_id, task_name):
    tasks = list_tasks(user_id, project_id).get("tasks", [])

    for t in tasks:
        if task_name.lower() in t.get("name", "").lower():
            return t

    return None