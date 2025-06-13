from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

user_cards = Table(
    "user_cards", Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("card_id", ForeignKey("cards.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    discord_id = Column(String, unique=True)
    username = Column(String)
    balance = Column(Integer, default=0)

    cards = relationship("Card", secondary=user_cards, back_populates="owners")
    boosters = relationship("Booster", back_populates="owner")

class Card(Base):
    __tablename__ = "cards"
    id = Column(String, primary_key=True)
    name = Column(String)
    price_usd = Column(Float)
    img_url = Column(String)

    owners = relationship("User", secondary=user_cards, back_populates="cards")

class Booster(Base):
    __tablename__ = "boosters"
    id = Column(Integer, primary_key=True)
    set_id = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="boosters")
