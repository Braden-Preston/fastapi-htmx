from typing import List, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Field, Session, SQLModel, Relationship, create_engine, select

# ----------------- Hero Models ---------------- #


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    team: Optional["Team"] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None = None


# ----------------- Team Models ---------------- #


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamRead(TeamBase):
    id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroReadWithTeam(HeroRead):
    team: TeamRead | None = None


class TeamReadWithHeroes(TeamRead):
    heroes: list[HeroRead] = []


# ------------ FastAPI App Instance ------------ #

postgres_url = f'postgresql://user:pass@localhost:5432/fastapi_dev'
engine = create_engine(postgres_url, echo=True)


def create_db_and_tables():
    print('Creating tables...')
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


app = FastAPI(debug=True)


async def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
    # with Session(engine) as session:
    #     yield


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ----------------- Hero Routes ---------------- #


@app.get("/heroes", response_model=list[HeroRead])
def get_heroes(
        *,
        offset: int = 0,
        limit: int = Query(default=100, ge=0, le=100),
        session: Session = Depends(get_session),
):
    query = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(query).all()
    return heroes


@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heros/{hero_id}", response_model=HeroReadWithTeam)
def get_hero(
        *,
        hero_id: int,
        session: Session = Depends(get_session),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    else:
        return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(
        *,
        hero_id: int,
        session: Session = Depends(get_session),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
        *,
        hero_id: int,
        hero_form: HeroUpdate,
        session: Session = Depends(get_session),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(404, "Hero not found")
    hero_data = hero_form.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


# ----------------- Team Routes ---------------- #


@app.get("/teams", response_model=list[TeamRead])
def get_teams(
        *,
        offset: int = 0,
        limit: int = Query(default=100, ge=0, le=100),
        session: Session = Depends(get_session),
):
    query = select(Team).offset(offset).limit(limit)
    teams = session.exec(query).all()
    return teams


@app.post("/teams", response_model=TeamRead)
def create_team(
        *,
        team_form: TeamCreate,
        session: Session = Depends(get_session),
):
    team = Team.from_orm(team_form)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.get("/teams/{team_id}", response_model=TeamReadWithHeroes)
def get_team(
        *,
        team_id: int,
        session: Session = Depends(get_session),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    return team


@app.delete("/teams/{team_id}")
def delete_team(
        *,
        team_id: int,
        session: Session = Depends(get_session),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    session.delete(team)
    session.commit()
    return {"ok", True}


@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
        *,
        team_id: int,
        team_form: TeamUpdate,
        session: Session = Depends(get_session),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team
