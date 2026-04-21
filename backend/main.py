from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Any, Dict
from tools.zoho_client import ZohoClient

from graph import graph   # ✅ LangGraph

from auth.routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
    same_site="lax",   # ✅ change from "none" → "lax"
    https_only=False
)
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

    user_id = request.session.get("user_id")

    if not user_id:
        return {
            "response": "User not authenticated. Please login again.",
            "pending_action": None
        }

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
    state["message"] = req.message

    result = graph.invoke(state)

    context_store[user_id] = result

    # ✅ NORMALIZE RESPONSE HERE
    response_text = ""
    pending_action = None

    res = result.get("response")

    # Case 1: QueryAgent → Zoho data (object)
    if isinstance(res, dict) and "projects" in res:
        projects = res.get("projects", [])
        if projects:
            response_text = "Here are your projects:\n" + "\n".join(
                [f"- {p['name']}" for p in projects]
            )
        else:
            response_text = "No projects found"

    elif isinstance(res, dict) and "tasks" in res:
        tasks = res.get("tasks", [])
        if tasks:
            response_text = "Here are your tasks:\n" + "\n".join(
                [f"- {t['name']} (ID: {t['id_string']})" for t in tasks]
            )
        else:
            response_text = "No tasks found"

    # Case 2: ActionAgent format
    elif isinstance(res, dict) and "message" in res:
        response_text = res["message"]

        if res.get("requires_confirmation"):
            pending_action = {
                "message": res["message"]
            }

    # Case 3: simple string
    elif isinstance(res, str):
        response_text = res

    else:
        response_text = "Unexpected response format"

    return {
        "response": response_text,
        "pending_action": pending_action
    }


@app.get("/projects")
def get_projects(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return {"error": "Not authenticated"}

    client = ZohoClient(user_id=user_id)
    return client.get_projects()