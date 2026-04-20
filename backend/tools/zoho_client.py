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