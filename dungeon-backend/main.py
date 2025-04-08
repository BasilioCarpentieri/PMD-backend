from fastapi import FastAPI, Body, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from supabase_client import save_session
from fastapi.openapi.utils import get_openapi
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Dungeon Master RPG API",
    description="API for starting interactive RPG sessions.",
    version="1.0.0",
)

# Environment API key
API_KEY = os.getenv("API_KEY")

# Bearer token validator
def validate_api_key(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Input model
class NewChatRequest(BaseModel):
    player_name: str
    genre: str
    prompt_input: str
    session_data: Optional[dict] = None

# Response model
class NewChatResponse(BaseModel):
    status: str
    session: Optional[dict] = None

# Protected route with Bearer Auth
@app.post("/createNewChat", response_model=NewChatResponse, dependencies=[Depends(validate_api_key)])
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

# OpenAPI schema override
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
