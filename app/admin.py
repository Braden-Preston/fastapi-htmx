from sqladmin import Admin, ModelView

from .models import Hero, Team


class HeroAdmin(ModelView, model=Hero):
    column_list = [Hero.id, Hero.name, Hero.secret_name]


class TeamAdmin(ModelView, model=Team):
    column_list = [Hero.id, Team.name]


def init_admin(app, engine):
    admin = Admin(app, engine, base_url="/_")

    admin.add_view(HeroAdmin)
    admin.add_view(TeamAdmin)
