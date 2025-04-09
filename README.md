💡 Dungeon Master API v1.00 — Setup Guide

📊 Supabase Setup

We first set up a sessions table in Supabase, which is a serverless backend platform built on top of PostgreSQL. It's used to store persistent data like players, sessions, inventory, and more — all with an instant REST and realtime API.

sessions table structure:

id (UUID): the primary key, auto-generated

player_name (text): the name the player chooses

genre (text): the story genre

prompt_input (text): the starting narrative or prompt

session_data (JSON): optional data for storing game state

created_at (timestamp): automatically set when the session is created

Supabase provides the database + auto-generated API + access control (via RLS) in one place.

🌐 Render

We created a Web Service in Render, which hosts the FastAPI backend. Render gives us a public HTTPS URL, which we plug into our FastAPI main.py so GPT knows where to call your backend from.

Example:

"servers": [
  {
    "url": "https://pmd-backend-t7zt.onrender.com"
  }
]

📁 Project Files

Inside our local project folder, we created:

.env

Stores secrets like:

SUPABASE_URL

SUPABASE_KEY

API_KEY (used to authenticate GPT Action calls)

This file is never uploaded to GitHub.

main.py

Defines the FastAPI app, endpoints, input/output models

Secures the /createNewChat route with Bearer token

Generates the OpenAPI schema consumed by GPT

supabase_client.py

Connects to Supabase using the environment variables

Contains helper function save_session(...) to insert session data

Will later be expanded with get_session, update_xp, etc.

requirements.txt

Lists Python packages needed by the project:

fastapi
uvicorn
python-dotenv
supabase

🚀 GitHub

We uploaded the main.py, supabase_client.py, and requirements.txt to a new GitHub repository.This allows Render to pull the code automatically, re-deploy when commits happen, and acts as version control.

✨ Deploying to Render

In Render, we connected the GitHub repo and created a new Web Service.

We added the environment variables:

SUPABASE_URL, SUPABASE_KEY, API_KEY

After deploying, Render gives us a URL like:

https://pmd-backend-t7zt.onrender.com

🧙️ GPT Action Integration

We go to ChatGPT > My GPTs > Actions > Import from URLUse:

https://pmd-backend-t7zt.onrender.com/openapi.json

After importing the schema, we configure Authentication:

Auth Type: API Key

Method: Bearer

API Key: (same as the one saved in API_KEY on Render)

Now GPT knows how to send:

Authorization: Bearer <your_api_key>

And it can securely call your backend to start new RPG sessions.

✅ Summary

You now have:

A secure, scalable backend

A persistent session storage system

GPT Actions fully integrated

All connections locked with authentication

Welcome to version 1.00 — you're live!
