from django.shortcuts import render
from django.utils import timezone
from matches.models import Match
from django.views.generic import ListView


class MatchesOngoingListView(ListView):
    template_name = 'matches/matches_ongoing_list.html'
    model = Match

    def get_queryset(self):
        return super().get_queryset().filter(start_date__lte=timezone.now(), end_date=None)


class MatchesIncomingListView(ListView):
    template_name = 'matches/matches_incoming_list.html'
    model = Match

    def get_queryset(self):
        return super().get_queryset().filter(start_date__gt=timezone.now())


class MatchesPlayedListView(ListView):
    template_name = 'matches/matches_played_list.html'
    model = Match

    def get_queryset(self):
        return super().get_queryset().filter(end_date__lt=timezone.now())
