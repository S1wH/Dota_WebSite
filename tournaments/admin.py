from django.contrib import admin
from tournaments.models import Tournament, TournamentStage

# Register your models here.

admin.site.register(Tournament)
admin.site.register(TournamentStage)
