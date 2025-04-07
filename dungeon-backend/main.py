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

@app.get("/")
def root():
    return {"message": "Dungeon Master API is up."}

# Override OpenAPI schema to point GPT to the Render URL
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
            "url": "https://pmd-backend-7t7z.onrender.com",
            "description": "Render production server"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
