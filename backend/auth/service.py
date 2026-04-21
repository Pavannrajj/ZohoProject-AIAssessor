import requests
from config.settings import *
from models.user_tokens import user_tokens
import time

def exchange_code_for_token(code: str, user_id: str):
    response = requests.post(ZOHO_TOKEN_URL, params={
        "grant_type": "authorization_code",
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "redirect_uri": ZOHO_REDIRECT_URI,
        "code": code
    })

    data = response.json()

    user_tokens[user_id] = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_at": time.time() + int(data["expires_in"])
    }
    print(user_tokens)
    return data


def refresh_access_token(user_id: str):
    token_data = user_tokens[user_id]

    response = requests.post(ZOHO_TOKEN_URL, params={
        "grant_type": "refresh_token",
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "refresh_token": token_data["refresh_token"]
    })

    data = response.json()

    token_data["access_token"] = data["access_token"]
    token_data["expires_at"] = time.time() + int(data["expires_in"])

    return token_data


def get_valid_token(user_id: str):
    if user_id not in user_tokens:
        raise Exception("User not logged in")

    token_data = user_tokens[user_id]

    if time.time() > token_data["expires_at"]:
        return refresh_access_token(user_id)["access_token"]

    return token_data["access_token"]