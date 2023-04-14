from django.contrib import admin
from matches.models import Match, MatchPeriod, PlayerStats

# Register your models here.
admin.site.register(Match)
admin.site.register(MatchPeriod)
admin.site.register(PlayerStats)
