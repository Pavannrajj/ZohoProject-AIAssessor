from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from auth.utils import get_auth_url
from auth.service import exchange_code_for_token

router = APIRouter()

@router.get("/login")
def login():
    return RedirectResponse(get_auth_url())


@router.get("/callback")
def callback(code: str, request: Request):
    # ✅ generate user_id (temporary unique id)
    user_id = "user_" + code[:8]

    # store token
    exchange_code_for_token(code, user_id)

    # ✅ save user in session
    request.session["user_id"] = user_id

    return RedirectResponse(url="http://localhost:5173/?auth=success")