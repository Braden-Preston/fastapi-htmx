# from typing import Optional

# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio.engine import create_async_engine
# from sqlalchemy.ext.asyncio.session import AsyncSession
# from sqlalchemy.orm.session import sessionmaker
# from sqlmodel import Field, SQLModel


# class HeroBase(SQLModel):
#     name: str = Field(index=True)
#     secret_name: str
#     age: Optional[int] = Field(default=None, index=True)


# class Hero(HeroBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)


# class HeroCreate(HeroBase):
#     pass


# class HeroRead(HeroBase):
#     id: int


# db_uri = 'postgresql+asyncpg://user:pass@localhost:5432/fastapi_dev'
# engine = create_async_engine(db_uri, future=True)
# session_maker = sessionmaker(
#     engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# app = FastAPI()


# async def get_session() -> AsyncSession:
#     session = session_maker()
#     try:
#         yield session
#     finally:
#         await session.close()


# @app.on_event('startup')
# async def initialize_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)


# @app.get('/heros')
# async def get_heros(
#         session: AsyncSession = Depends(get_session)):
#     heroes = await session.get
#     #         heroes = session.exec(select(Hero)).all()
# #         return heroes#         heroes = session.exec(select(Hero)).all()
# #         return heroes

# @app.post('/heros', response_model=HeroRead)
# async def create_hero(
#         hero: HeroCreate,
#         session: AsyncSession = Depends(get_session),
# ):
#     new_hero = Hero.from_orm(hero)
#     session.add(new_hero)
#     await session.commit()
#     return new_hero


# from typing import List, Optional

# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio.engine import create_async_engine
# from sqlalchemy.ext.asyncio.session import AsyncSession
# from sqlalchemy.orm.session import sessionmaker
# from sqlmodel import Field, Session, SQLModel, select

# postgres_url = f'postgresql+asyncpg://user:pass@localhost:5432/'
# engine = create_async_engine(postgres_url, echo=True)
# session_maker = sessionmaker(engine,
#                              expire_on_commit=False,
#                              class_=AsyncSession)

# # def create_db_and_tables():
# #     SQLModel.metadata.drop_all()
# #     SQLModel.metadata.create_all(engine, checkfirst=True)

# app = FastAPI()

# @app.on_event('startup')
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)

#     # create_db_and_tables()

# async def get_session() -> AsyncSession:
#     session = session_maker()
#     try:
#         yield session
#     finally:
#         await session.close()

# class HeroBase(SQLModel):
#     name: str = Field(index=True)
#     secret_name: str
#     age: Optional[int] = Field(default=None, index=True)

# class Hero(HeroBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

# class HeroCreate(HeroBase):
#     pass

# class HeroRead(HeroBase):
#     id: int

# @app.post(
#     '/heroes/',
#     dependencies='Create a new hero',
#     response_model=HeroRead,
# )
# async def create_hero(
#         hero: HeroCreate,
#         session: AsyncSession = Depends(get_session),
# ):
#     session.add(hero)
#     await session.commit()
#     await session.refresh(hero)
#     return hero
#     # with Session(engine) as session:
#     #     db_hero = Hero.from_orm(hero)
#     #     session.add(db_hero)
#     #     session.commit()
#     #     session.refresh(db_hero)
#     #     return db_hero

# @app.get('/heroes/', response_model=List[HeroRead])
# def read_heroes():
#     with Session(engine) as session:
#         heroes = session.exec(select(Hero)).all()
#         return heroes
