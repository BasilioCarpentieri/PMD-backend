from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
from supabase_client import save_session
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Dungeon Master RPG API",
    description="API for starting interactive RPG sessions.",
    version="1.0.0",
)

# Input model
class NewChatRequest(BaseModel):
    player_name: str
    genre: str
    prompt_input: str
    session_data: Optional[dict] = None  # Allow this to be None

# Response model (now allows session=None to avoid 500 if save_session returns nothing)
class NewChatResponse(BaseModel):
    status: str
    session: Optional[dict] = None

@app.post("/createNewChat", response_model=NewChatResponse)
def create_new_chat(data: NewChatRequest = Body(...)):
    saved = save_session(
        data.player_name,
        data.genre,
        data.prompt_input,
        data.session_data or {}
    )
    return {"status": "success", "session": saved}

@app.get("/")
def root():
    return {"message": "Dungeon Master API is up."}

# Custom OpenAPI schema (correct server)
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
            "url": "https://pmd-backend-t7zt.onrender.com",
            "description": "Render production server"
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
