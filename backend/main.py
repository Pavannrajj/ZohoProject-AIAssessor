from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict
from tools.zoho_client import ZohoClient

from graph import graph   # ✅ LangGraph

from auth.routes import router as auth_router

app = FastAPI()

# OAuth routes (unchanged)
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    return {"message": "API is running"}


# Request / Response models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: Any
    pending_action: Any = None


# ✅ Simple in-memory state (per user)
context_store: Dict[str, Dict] = {}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request):

    user_id = "demo_user"   # later replace with real auth user

    # ✅ Initialize or reuse state
    if user_id not in context_store:
        context_store[user_id] = {
            "message": "",
            "user_id": user_id,
            "project_id": None,
            "intent": None,
            "pending_action": None,
            "response": None
        }

    state = context_store[user_id]

    # ✅ Update message only (keep memory like project_id)
    state["message"] = req.message

    # ✅ Run LangGraph
    result = graph.invoke(state)

    # ✅ Save updated state back
    context_store[user_id] = result

    print("Message:", req.message)
    print("Intent:", result.get("intent"))

    return {
        "response": result.get("response"),
        "pending_action": result.get("pending_action")
    }

@app.get("/projects")
def get_projects():
    client = ZohoClient(user_id="demo_user")
    return client.get_projects()