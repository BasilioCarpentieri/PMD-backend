from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def save_session(player_name, genre, prompt_input, session_data):
    response = supabase.table("sessions").insert({
        "player_name": player_name,
        "genre": genre,
        "prompt_input": prompt_input,
        "session_data": session_data
    }).execute()

    # Always return something safe
    if response.data and isinstance(response.data, list) and len(response.data) > 0:
        return response.data[0]
    return {"note": "Session saved but no data returned."}
