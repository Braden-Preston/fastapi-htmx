from fastapi import Header, HTTPException
from sqlmodel import Session

from .database import engine


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
