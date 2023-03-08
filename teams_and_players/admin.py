from django.contrib import admin
from teams_and_players.models import Team, Player, CareerPeriod

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(CareerPeriod)
