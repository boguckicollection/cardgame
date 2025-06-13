from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import User
from sqlalchemy import select
import os

app = FastAPI(title="Cardgame API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8000/callback")
OAUTH_URL = (
    "https://discord.com/api/oauth2/authorize?response_type=code"
    f"&client_id={CLIENT_ID}&scope=identify&redirect_uri={REDIRECT_URI}"
)

@app.get("/login")
async def login():
    return RedirectResponse(OAUTH_URL)

@app.get("/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "missing code"}
    return {"code": code}

@app.get("/profile/{discord_id}")
async def get_profile(discord_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.discord_id == discord_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "not found"}
    return {
        "username": user.username,
        "balance": user.balance,
        "boosters": [b.set_id for b in user.boosters],
        "cards": [c.id for c in user.cards],
    }

@app.get("/ranking")
async def get_ranking():
    return []

@app.get("/shop")
async def get_shop():
    return []

@app.get("/giveaway")
async def get_giveaway():
    return []
