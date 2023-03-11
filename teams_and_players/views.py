from django.shortcuts import render
from teams_and_players.models import Player, Team


def teams_view(request):
    teams = Team.objects.all()

    return render(request, 'teams_and_players/teams.html', context={'teams': teams})


def players_view(request):
    players = Player.objects.all()
    return render(request, 'teams_and_players/players.html', context={'players': players})
