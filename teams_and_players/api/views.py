from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from teams_and_players.models import Team, Player, CareerPeriod
from teams_and_players.api.serializers import (
    TeamSerializer,
    PlayerSerializer,
    CareerPeriodSerializer,
)


class TeamViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["win_matches", "lose_matches", "prize", "country"]


class PlayerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filterset_fields = ["country"]


class CareerPeriodViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CareerPeriod.objects.all().select_related(
        "player",
        "team",
    )
    serializer_class = CareerPeriodSerializer
    filterset_fields = ["role", "player", "team"]
