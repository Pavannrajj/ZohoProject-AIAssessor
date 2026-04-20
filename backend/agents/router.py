def route(message: str):
    message = message.lower()

    if any(word in message for word in ["create", "delete", "update"]):
        return "action"
    else:
        return "query"