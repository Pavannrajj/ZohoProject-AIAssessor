from .zoho_client import ZohoClient

def list_projects(user_id):
    client = ZohoClient(user_id)
    return client.get_projects()

def list_tasks(user_id, project_id):
    client = ZohoClient(user_id)
    return client.get_tasks(project_id)

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
    return client.update_task(project_id, task_id, data)

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