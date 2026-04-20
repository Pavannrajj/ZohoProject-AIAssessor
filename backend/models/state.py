# models/state.py

from typing import TypedDict, Optional, Dict, Any

class GraphState(TypedDict):
    message: str
    user_id: str

    # routing
    intent: Optional[str]

    # memory
    project_id: Optional[str]

    # HIL
    pending_action: Optional[Dict[str, Any]]

    # response
    response: Optional[str]