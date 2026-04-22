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
    user_id = exchange_code_for_token(code)

    request.session["user_id"] = user_id

    return RedirectResponse(url="http://localhost:5173/?auth=success")


@router.get("/logout")
def logout(request: Request):

    user_id = request.session.get("user_id")  # ✅ get first

    request.session.clear()  # then clear

    from models.user_tokens import user_tokens

    if user_id and user_id in user_tokens:
        user_tokens.pop(user_id)

    return RedirectResponse(url="http://localhost:5173/")