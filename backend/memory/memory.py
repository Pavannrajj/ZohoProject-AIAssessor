from supabase import create_client

from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_memory(user_id: str, key: str, value: str):
    supabase.table("user_memory").insert({
        "user_id": user_id,
        "key": key,
        "value": value
    }).execute()


def get_memory(user_id: str, key: str):
    res = supabase.table("user_memory") \
        .select("value") \
        .eq("user_id", user_id) \
        .eq("key", key) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    if res.data:
        return res.data[0]["value"]

    return None