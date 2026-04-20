from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from auth.utils import get_auth_url
from auth.service import exchange_code_for_token

router = APIRouter()

# Step 1: Login
@router.get("/login")
def login():
    return RedirectResponse(get_auth_url())

# Step 2: Callback
@router.get("/callback")
def callback(code: str):
    user_id = "demo_user"  # later replace with real session user
    exchange_code_for_token(code, user_id)
    return {"message": "Login successful"}