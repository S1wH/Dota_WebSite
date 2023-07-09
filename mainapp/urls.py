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
from mainapp.views import (
    index_view,
    SearchNewsListView,
    SearchTeamsListView,
    SearchMatchesListView,
    SearchPlayersListView,
)

app_name = "mainapp"

urlpatterns = [
    path("", index_view, name="index"),
    path("search/news/", SearchNewsListView.as_view(), name="search_news"),
    path("search/players/", SearchPlayersListView.as_view(), name="search_players"),
    path("search/teams/", SearchTeamsListView.as_view(), name="search_teams"),
    path("search/matches/", SearchMatchesListView.as_view(), name="search_matches"),
]
