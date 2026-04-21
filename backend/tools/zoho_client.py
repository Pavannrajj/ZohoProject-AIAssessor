import token
from urllib import response
from wsgiref import headers

import requests
from auth.service import get_valid_token
from models.user_tokens import user_tokens

from dotenv import load_dotenv
import os

load_dotenv()

ZOHO_PORTAL_ID = os.getenv("ZOHO_PORTAL_ID")
class ZohoClient:

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.access_token = get_valid_token(user_id)

        self.portal_id = user_tokens[user_id]["portal_id"]

    def get_projects(self):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": response.text}
        return response.json()
    
    def get_tasks(self, project_id: str):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/tasks/"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return {"error": response.text}

        return response.json()

    def delete_task(self, project_id: str, task_id: str):
        token = get_valid_token(self.user_id)

        headers = {
            "Authorization": f"Zoho-oauthtoken {token}"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/tasks/{task_id}/"

        response = requests.delete(url, headers=headers)

        if response.status_code not in [200, 204]:
            return {"error": response.text}

        return {"message": f"Task {task_id} deleted successfully"}
    
    def create_task(self, project_id: str, task_name: str):
        token = get_valid_token(self.user_id)

        headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/x-www-form-urlencoded"
        }

        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/tasks/"

        data = {
        "name": task_name
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code not in [200, 201]:
            return {"error": response.text}

        return response.json()
    
    def headers(self):
        from auth.service import get_valid_token

        access_token = get_valid_token(self.user_id)

        return {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        }

    def get_task_details(self, project_id, task_id):
        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/tasks/{task_id}/"

        response = requests.get(url, headers=self.headers())

        if response.status_code != 200:
            return {
            "status": "error",
            "message": "Failed to fetch task details",
            "details": response.text
            }

        return response.json()
    

    def update_task(self, project_id, task_id, data):
        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/tasks/{task_id}/"

        response = requests.post(
        url,
        headers={
            "Authorization": f"Zoho-oauthtoken {get_valid_token(self.user_id)}"
        },
        data={
            "_method": "PUT",        # ✅ IMPORTANT
            "name": data["name"]     # ✅ correct field
        }
    )

        print("UPDATE RESPONSE:", response.text)

        if response.status_code not in [200, 201]:
            return {
            "status": "error",
            "message": "Failed to update task",
            "details": response.text
        }

        return response.json()
    

    def get_project_members(self, project_id):
        url = f"https://projectsapi.zoho.in/restapi/portal/{self.portal_id}/projects/{project_id}/users/"

        response = requests.get(
        url,
        headers={
            "Authorization": f"Zoho-oauthtoken {get_valid_token(self.user_id)}"
        }
    )
        print("MEMBERS RESPONSE:", response.status_code, response.text)
        if response.status_code != 200:
            return {
            "status": "error",
            "message": "Failed to fetch project members",
            "details": response.text
        }

        return response.json()