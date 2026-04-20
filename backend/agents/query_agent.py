from tools.zoho_client import ZohoClient

class QueryAgent:
    def handle(self, message: str, user_id: str):
        client = ZohoClient(user_id)

        message = message.lower()

        if "projects" in message:
            data = client.get_projects()
            return f"Projects: {data}"

        elif "tasks" in message:
            # placeholder (you'll implement later)
            return "Fetching tasks (not implemented yet)"

        return "QueryAgent: Could not understand request"