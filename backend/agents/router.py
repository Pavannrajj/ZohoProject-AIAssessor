def route(message: str):
    if "create" in message or "delete" in message:
        return "action"
    return "query"