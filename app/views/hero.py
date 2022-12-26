from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..depends import get_token_header, get_session
from ..models import Hero, HeroCreate, HeroRead, HeroReadWithTeam, HeroUpdate

router = APIRouter(
    prefix="/heroes",
    dependencies=[
        # Depends(get_token_header),
    ],
)


@router.get("/", response_model=list[HeroRead])
def get_heroes(
        *,
        offset: int = 0,
        limit: int = Query(default=100, ge=0, le=100),
        session: Session = Depends(get_session),
):
    query = select(Hero).offset(offset).limit(limit)
    heroes = session.exec(query).all()
    return heroes


@router.post("/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/{hero_id}", response_model=HeroReadWithTeam)
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


@router.delete("/{hero_id}")
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


@router.patch("/{hero_id}", response_model=HeroRead)
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
