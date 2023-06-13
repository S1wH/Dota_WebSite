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
from teams_and_players import views

app_name = "teams_and_players_app"

urlpatterns = [
    # player urls
    path("players/", views.PlayerListView.as_view(), name="player_list"),
    path("players/<int:pk>/", views.PlayerDetailView.as_view(), name="one_player"),
    path("players/create/", views.PlayerCreateView.as_view(), name="create_player"),
    path(
        "players/update/<int:pk>/",
        views.PlayerUpdateView.as_view(),
        name="update_player",
    ),
    path(
        "players/delete/<int:pk>/",
        views.PlayerDeleteView.as_view(),
        name="delete_player",
    ),
    # career period urls
    path("career_period/create/", views.create_career_view, name="create_career"),
    # team urls
    path("teams/", views.TeamListView.as_view(), name="team_list"),
    path("teams/<int:pk>/", views.TeamDetailView.as_view(), name="one_team"),
    path("teams/create/", views.TeamCreateView.as_view(), name="create_team"),
    path("teams/update/<int:pk>/", views.TeamUpdateView.as_view(), name="update_team"),
    path("teams/delete/<int:pk>/", views.TeamDeleteView.as_view(), name="delete_team"),
]
