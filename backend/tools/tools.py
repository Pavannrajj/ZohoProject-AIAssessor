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