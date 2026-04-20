import token
from urllib import response
from wsgiref import headers

import requests
from auth.service import get_valid_token

class ZohoClient:

    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_projects(self):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = "https://projectsapi.zoho.in/restapi/portal/pavanbdotofficial5gmaildotcom/projects/"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": response.text}
        return response.json()
    
    def get_tasks(self, project_id: str):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/pavanbdotofficial5gmaildotcom/projects/{project_id}/tasks/"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": response.text}

        return response.json()

    def delete_task(self, project_id: str, task_id: str):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/pavanbdotofficial5gmaildotcom/projects/{project_id}/tasks/{task_id}/"

        response = requests.delete(url, headers=headers)

        if response.status_code not in [200, 204]:
            return {"error": response.text}

        return {"message": f"Task {task_id} deleted successfully"}