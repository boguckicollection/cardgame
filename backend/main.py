from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
import json
import os

from database import get_session
from models import User
import httpx

app = FastAPI(title="Cardgame API")


@app.get("/")
async def read_root():
    """Health check endpoint for quick verification."""
    return {"Hello": "CardCollectorGame Backend running!"}

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

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
with open(DATA_DIR / "sets.json", "r") as f:
    ALL_SETS = json.load(f)
with open(DATA_DIR / "price.json", "r") as f:
    BASE_PRICE = json.load(f)

SHOP_ITEMS = [
    {
        "id": s["id"],
        "name": s["name"],
        "logo": s.get("images", {}).get("logo"),
        "price": int(BASE_PRICE.get(s["id"], 0) * 1.5),
    }
    for s in ALL_SETS[:20]
]

@app.get("/login")
async def login():
    return RedirectResponse(OAUTH_URL)

@app.get("/callback")
async def oauth_callback(request: Request, session: AsyncSession = Depends(get_session)):
    code = request.query_params.get("code")
    if not code:
        return {"error": "missing code"}

    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://discord.com/api/oauth2/token",
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_json = token_resp.json()
        access_token = token_json.get("access_token")
        if not access_token:
            return {"error": "invalid token"}

        user_resp = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_resp.json()

    result = await session.execute(select(User).where(User.discord_id == user_data["id"]))
    user = result.scalar_one_or_none()
    if not user:
        user = User(discord_id=user_data["id"], username=user_data.get("username", ""))
        session.add(user)
        await session.commit()

    html_content = f"<script>localStorage.setItem('userId', '{user.discord_id}'); window.location.href='/profile.html';</script>"
    return HTMLResponse(content=html_content)

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
    return SHOP_ITEMS

@app.get("/giveaway")
async def get_giveaway():
    return []
