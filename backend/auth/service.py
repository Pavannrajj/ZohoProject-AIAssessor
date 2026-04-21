import requests
from config.settings import *
from models.user_tokens import user_tokens
import time

def get_portals(access_token):
    response = requests.get(
        "https://projectsapi.zoho.in/restapi/portals/",   # ✅ FIXED
        headers={
            "Authorization": f"Zoho-oauthtoken {access_token}"
        }
    )

    print("PORTALS RESPONSE:", response.status_code, response.text)

    return response.json()

def exchange_code_for_token(code: str, user_id: str):

    # Step 1: Get access token
    response = requests.post(
        ZOHO_TOKEN_URL,
        params={
            "grant_type": "authorization_code",
            "client_id": ZOHO_CLIENT_ID,
            "client_secret": ZOHO_CLIENT_SECRET,
            "redirect_uri": ZOHO_REDIRECT_URI,
            "code": code
        }
    )

    data = response.json()

    access_token = data.get("access_token")

    if not access_token:
        raise Exception(f"Failed to get access token: {data}")

    # Step 2: Fetch portals
    portals_data = get_portals(access_token) 

    

    print("PORTALS RESPONSE:", portals_data)

    # Step 3: Validate response
    if "portals" not in portals_data or not portals_data["portals"]:
        raise Exception(f"Portal fetch failed: {portals_data}")

    portal_id = portals_data["portals"][0]["id"]

    # Step 4: Store everything
    user_tokens[user_id] = {
        "access_token": access_token,
        "refresh_token": data.get("refresh_token"),
        "expires_at": time.time() + int(data["expires_in"]),
        "portal_id": portal_id
    }

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