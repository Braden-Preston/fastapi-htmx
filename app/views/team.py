from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..depends import get_token_header, get_session
from ..models import Team, TeamCreate, TeamRead, TeamReadWithHeroes, TeamUpdate

router = APIRouter(
    prefix="/teams",
    dependencies=[
        # Depends(get_token_header)
        Depends(get_session)
    ],
)


@router.get("/", response_model=list[TeamRead])
def get_teams(
        *,
        offset: int = 0,
        limit: int = Query(default=100, ge=0, le=100),
        session: Session = Depends(get_session),
):
    query = select(Team).offset(offset).limit(limit)
    teams = session.exec(query).all()
    return teams


@router.post("/", response_model=TeamRead)
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


@router.get("/{team_id}", response_model=TeamReadWithHeroes)
def get_team(
        *,
        team_id: int,
        session: Session = Depends(get_session),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(404, "Team not found")
    return team


@router.delete("/{team_id}")
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


@router.patch("/{team_id}", response_model=TeamRead)
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
