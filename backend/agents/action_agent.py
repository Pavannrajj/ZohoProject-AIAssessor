from tools.zoho_client import ZohoClient

class ActionAgent:
    def handle(self, message: str, user_id: str):
        client = ZohoClient(user_id)

        message = message.lower()

        if "create task" in message:
            # placeholder
            return "Task creation flow (confirmation needed)"

        elif "delete task" in message:
            # placeholder
            return "Delete confirmation required"

        return "ActionAgent: Could not understand request"