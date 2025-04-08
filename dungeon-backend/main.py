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

# Request schema
class NewChatRequest(BaseModel):
    player_name: str
    genre: str
    prompt_input: str
    session_data: Optional[dict] = None

# Response schema
class NewChatResponse(BaseModel):
    status: str
    session: dict

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

# Custom OpenAPI schema for GPT integration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add GPT-specific metadata for auto-approval
    if "/createNewChat" in openapi_schema["paths"]:
        post_op = openapi_schema["paths"]["/createNewChat"]["post"]
        post_op["x-openai"] = {
            "name_for_model": "start_rpg_session",
            "description_for_model": "Starts a new RPG session with a player name, genre, and story prompt. No approval needed.",
            "parameters": {
                "player_name": {
                    "type": "string",
                    "description": "The name of the player."
                },
                "genre": {
                    "type": "string",
                    "description": "The genre of the RPG story."
                },
                "prompt_input": {
                    "type": "string",
                    "description": "The setup for the story, like a scene or environment."
                }
            }
        }

    # Set correct public URL for schema
    openapi_schema["servers"] = [
        {
            "url": "https://pmd-backend-t7zt.onrender.com",
            "description": "Render production server"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
