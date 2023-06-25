from django.utils import timezone
from django.views.generic import ListView
from matches.models import Match


def get_related_info(query_set):
    return query_set.select_related(
        "team1", "team2", "tournament_stage", "tournament_stage__tournament"
    ).prefetch_related("match_period")


class MatchesOngoingListView(ListView):
    template_name = "matches/matches_ongoing_list.html"
    paginate_by = 15
    model = Match

    def get_queryset(self):
        return get_related_info(
            super().get_queryset().filter(start_date__lte=timezone.now(), end_date=None)
        )


class MatchesIncomingListView(ListView):
    template_name = "matches/matches_incoming_list.html"
    paginate_by = 15
    model = Match

    def get_queryset(self):
        return get_related_info(
            super().get_queryset().filter(start_date__gt=timezone.now())
        )


class MatchesPlayedListView(ListView):
    template_name = "matches/matches_played_list.html"
    paginate_by = 15
    model = Match

    def get_queryset(self):
        return get_related_info(
            super().get_queryset().filter(end_date__lt=timezone.now())
        )
