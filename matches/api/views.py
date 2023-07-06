from rest_framework import viewsets, mixins
from matches.models import Match, MatchPeriod
from matches.api.serializers import MatchSerializer, MatchPeriodSerializer


class MatchViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Match.objects.all().select_related(
        'team1',
        'team2',
        'winner',
        'loser'
    )
    serializer_class = MatchSerializer
    filterset_fields = ['start_date', 'end_date']


class MatchPeriodViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = MatchPeriod.objects.all().select_related(
        'win_team',
        'match',
    ).select_related(
        'match__team1',
        'match__team2',
        'match__winner',
        'match__loser',
    )
    serializer_class = MatchPeriodSerializer
    filterset_fields = ['match', 'win_team']
