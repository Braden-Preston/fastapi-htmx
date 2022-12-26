from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.testclient import TestClient
from sqlmodel import (Field, Relationship, Session, SQLModel, create_engine,
                      select)

from .database import create_db_and_tables
from .views.hero import router as hero_router
from .views.team import router as team_router

app = FastAPI(debug=True)

app.include_router(hero_router)
app.include_router(team_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello FastAPI 👋!"}


client = TestClient(app)
