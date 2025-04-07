from fastapi import FastAPI, Request
from pydantic import BaseModel
from supabase_client import save_session
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Dungeon Master RPG API",
    description="API for starting interactive RPG sessions.",
    version="1.0.0",
)

class NewChatRequest(BaseModel):
    player_name: str
    genre: str
    prompt_input: str
    session_data: dict

@app.post("/createNewChat")
def create_new_chat(data: NewChatRequest):
    saved = save_session(
        data.player_name,
        data.genre,
        data.prompt_input,
        data.session_data
    )
    return {"status": "success", "session": saved}

# Root route (optional, just for testing)
@app.get("/")
def root():
    return {"message": "Dungeon Master API is up."}

# Override OpenAPI schema with `servers` key
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {
            "url": "https://5c68cd04-07dc-4578-8794-60b83d8d50ed-00-21n85gz2g9qt6.spock.replit.dev",
            "description": "Replit production server"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
