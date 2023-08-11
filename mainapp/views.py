from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from celery.result import AsyncResult
from news.models import News
from mainapp.models import QueueTask
from teams_and_players.models import Team, Player
from teams_and_players.views import PlayerListView, TeamListView
from matches.models import Match
from matches.views import (
    MatchesPlayedListView,
    MatchesIncomingListView,
    MatchesOngoingListView,
)
from my_dota.celery import app

SEARCH = "search"


def index_view(request):
    videos = ["highlight.mp4", "highlight.mp4", "highlight.mp4", "highlight.mp4"]
    return render(
        request,
        "mainapp/index.html",
        context={"main_news": News.important_news(), "videos": videos},
    )


class TasksListView(ListView):
    model = QueueTask
    template_name = "mainapp/tasks.html"

    def get_queryset(self):
        tasks = QueueTask.objects.all()
        for task in tasks:
            task.status = AsyncResult(task.task_id, app=app).status
            task.save()
        return tasks


class SearchTeamsListView(ListView):
    model = Team
    template_name = "mainapp/search_teams.html"

    def get_queryset(self):
        prev_search = cache.get(SEARCH)
        return TeamListView.get_queryset(TeamListView()).filter(
            name__icontains=prev_search
        )


class SearchPlayersListView(ListView):
    model = Player
    template_name = "mainapp/search_players.html"

    def get_queryset(self):
        prev_search = cache.get(SEARCH)
        return PlayerListView.get_queryset(PlayerListView()).filter(
            Q(name__icontains=prev_search) | Q(nickname__icontains=prev_search)
        )


class SearchMatchesListView(ListView):
    model = Match
    paginate_by = 15
    template_name = "mainapp/search_matches.html"

    def get_queryset(self):
        prev_search = cache.get(SEARCH)
        return (
                MatchesOngoingListView.get_queryset(MatchesOngoingListView())
                | MatchesIncomingListView.get_queryset(MatchesIncomingListView())
                | MatchesPlayedListView.get_queryset(MatchesPlayedListView())
        ).filter(
            Q(team1__name__icontains=prev_search)
            | Q(team2__name__icontains=prev_search)
        )


class SearchNewsListView(ListView):
    model = News
    template_name = "mainapp/search_news.html"

    def get_queryset(self):
        prev_search = cache.get(SEARCH)
        query = self.request.GET.get("s")
        if query:
            cache.set(SEARCH, query)
        else:
            query = prev_search
        return News.objects.all().filter(
            Q(author__nickname__icontains=query) | Q(header__icontains=query)
        )
