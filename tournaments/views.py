from django.views.generic import ListView, DetailView
from django.utils import timezone
from tournaments.models import Tournament, TournamentStage


class TournamentsCurrentListView(ListView):
    template_name = "tournaments/tournaments_current_list.html"
    model = Tournament

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
        )


class TournamentsPreviousListView(ListView):
    template_name = "tournaments/tournaments_previous_list.html"
    model = Tournament

    def get_queryset(self):
        return super().get_queryset().filter(end_date__lt=timezone.now())


class TournamentsFutureListView(ListView):
    template_name = "tournaments/tournaments_future_list.html"
    model = Tournament

    def get_queryset(self):
        return super().get_queryset().filter(start_date__gt=timezone.now())


class TournamentDetailView(DetailView):
    model = Tournament

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["group_stage_table"] = (
            TournamentStage.objects.get(
                tournament=data["tournament"], stage=TournamentStage.GROUP_STAGE
            )
            .group_stage_table()
            .items()
        )
        return data
