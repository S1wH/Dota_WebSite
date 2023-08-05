from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from matches.models import Match, MatchPeriod
from matches.api.serializers import MatchSerializerV10, MatchSerializerV11, MatchPeriodSerializer
from my_dota.version import Version


class MatchViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Match.objects.all()
        .select_related("team1", "team2", "winner", "loser", "tournament_stage__tournament")
    )
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    ordering_fields = ["status", "format"]
    search_fields = ["winner__name"]
    versioning_class = Version

    def get_serializer_class(self):
        if self.request.version == 'v1.0':
            return MatchSerializerV10
        return MatchSerializerV11


class MatchPeriodViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        MatchPeriod.objects.all()
        .select_related(
            "win_team",
            "match",
        )
        .select_related(
            "match__team1",
            "match__team2",
            "match__winner",
            "match__loser",
        )
    )
    permission_classes = [IsAuthenticated]
    serializer_class = MatchPeriodSerializer
    filter_backends = [SearchFilter]
    search_fields = ["match__winner__name"]
    versioning_class = Version
