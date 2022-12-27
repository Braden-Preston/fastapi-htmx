from fastapi import FastAPI

from .admin import init_admin
from .database import engine
from .views.core import router as core_router
from .views.hero import router as hero_router
from .views.team import router as team_router

app = FastAPI(debug=True)

app.include_router(core_router)
app.include_router(hero_router)
app.include_router(team_router)

# Bind admin interface
admin = init_admin(app, engine)
