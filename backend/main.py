from fastapi import FastAPI
from pydantic import BaseModel

from agents.query_agent import QueryAgent
from agents.action_agent import ActionAgent
from agents.router import route

app = FastAPI()
query_agent = QueryAgent()
action_agent = ActionAgent()

@app.get("/")
async def root():
    return {"message": "API is running"}


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat")
async def chat(req: ChatRequest):
    agent_type = route(req.message)

    if agent_type == "action":
        result = action_agent.handle(req.message)
    else:
        result = query_agent.handle(req.message)

    return {"response": result}