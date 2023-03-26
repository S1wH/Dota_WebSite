"""my_dota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from teams_and_players import views as main_views

app_name = 'teams_and_players_app'

urlpatterns = [
    path('teams/', main_views.teams_view, name='teams'),
    path('players/', main_views.players_view, name='players'),
    path('teams/<int:team_id>/', main_views.get_one_team_view, name='one_team'),
    path('players/<int:player_id>/', main_views.get_one_player_view, name='one_player'),
    path('players/create/', main_views.create_player_view, name='create_player'),
    path('career_period/create/', main_views.create_career_view, name='create_career'),
]
