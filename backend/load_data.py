import json
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import engine, get_session
from models import Base, User, Card, Booster

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def load_json(filename):
    with open(DATA_DIR / filename, "r") as f:
        return json.load(f)

async def load_users(session: AsyncSession):
    users = load_json("users.json")
    for disc_id, info in users.items():
        user = User(discord_id=disc_id, username=info.get("username", ""), balance=info.get("coins", 0))
        session.add(user)
        for booster_set in info.get("boosters", []):
            session.add(Booster(set_id=booster_set, owner=user))
        for card in info.get("cards", []):
            c = await session.get(Card, card["id"])
            if not c:
                c = Card(id=card["id"], name=card["name"], price_usd=card.get("price_usd", 0), img_url=card.get("img_url"))
            user.cards.append(c)
    await session.commit()

async def main():
    await init_db()
    async for session in get_session():
        await load_users(session)

if __name__ == "__main__":
    asyncio.run(main())
