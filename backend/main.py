from fastapi import FastAPI, Request
from pydantic import BaseModel
from tools.zoho_client import ZohoClient

from agents.query_agent import QueryAgent
from agents.action_agent import ActionAgent
from agents.router import route

from auth.routes import router as auth_router

app = FastAPI()

# Include OAuth routes
app.include_router(auth_router, prefix="/auth")

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
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):
    """
    For now:
    - using static user_id
    - later replace with session/JWT user
    """
    user_id = "demo_user"

    agent_type = route(req.message)

    if agent_type == "action":
        result = action_agent.handle(req.message, user_id)
    else:
        result = query_agent.handle(req.message, user_id)

    return {"response": result}


@app.get("/projects")
def get_projects():
    client = ZohoClient(user_id="demo_user")
    return client.get_projects()