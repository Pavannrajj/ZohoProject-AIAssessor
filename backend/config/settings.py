import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env") 

ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")

ZOHO_AUTH_URL = os.getenv("ZOHO_AUTH_URL")
ZOHO_TOKEN_URL = os.getenv("ZOHO_TOKEN_URL")