from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

from sqlmodel import SQLModel, Session, create_engine

from .models import (Hero)

app = FastAPI(debug=True)

postgres_url = f'postgresql://localhost:5432/fastapi_dev?user=user&password=pass'
engine = create_engine(postgres_url, echo=True)
db = Session(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


class Role(str, Enum):
    owner = 'owner'
    admin = 'admin'
    user = 'user'


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: str | None = None):
    return {'item_id': item_id, 'q': q}


@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):

    return {'item_name': item.name, 'item_id': item_id}


@app.post('/heros/create')
def create_hero(hero: Hero = p):
    # with db:
    db.add(hero)
    db.commit()
    db.close()


class User(BaseModel):
    uid: str
    role: Role


@app.get('/users/{uid}', response_model=User)
def update_item(uid: int, role: Role):
    user = User(uid=uid, role=role)
    return user
