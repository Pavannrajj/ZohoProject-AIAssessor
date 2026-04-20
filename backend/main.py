from fastapi import FastAPI, Request
from pydantic import BaseModel
from tools.zoho_client import ZohoClient
from typing import Any

from agents.query_agent import QueryAgent
from agents.action_agent import ActionAgent
from agents.router import route

from auth.routes import router as auth_router

app = FastAPI()

# Include OAuth routes
app.include_router(auth_router, prefix="/auth")

# ✅ TEMP TEST (Step 1)


# Agents
query_agent = QueryAgent()
action_agent = ActionAgent()


@app.get("/")
async def root():
    return {"message": "API is running"}


# Request/Response models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: Any

context_store = {}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):

    user_id = "demo_user"
    message = req.message

    # ✅ initialize memory
    if user_id not in context_store:
        context_store[user_id] = {}

    context = context_store[user_id]

    from memory.store import pending_actions
    if user_id in pending_actions:
        decision = "action"
    else:
        decision = route(message)

    if decision == "action":
        result = action_agent.handle(user_id, message, context)
    else:
        result = query_agent.handle(user_id, message, context)
    print("Message:", message)
    print("Decision:", decision)
    return {"response": result}

@app.get("/projects")
def get_projects():
    
    client = ZohoClient(user_id="demo_user")
    return client.get_projects()