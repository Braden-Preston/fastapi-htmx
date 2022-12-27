from fastapi import APIRouter, Depends, HTTPException, Query

from ..database import create_db_and_tables
from ..depends import get_token_header, get_session

router = APIRouter(
    prefix="",
    dependencies=[
        # Depends(get_token_header),
    ],
)


@router.on_event("startup")
def on_startup():
    create_db_and_tables()


@router.get("/")
async def root():
    return {"message": "Hello FastAPI 👋!"}
