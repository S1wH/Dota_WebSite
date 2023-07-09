from rest_framework import serializers
from matches.models import Match, MatchPeriod
from teams_and_players.api.serializers import TeamSerializer


class MatchSerializer(serializers.ModelSerializer):
    team1 = TeamSerializer()
    team2 = TeamSerializer()
    winner = TeamSerializer()
    loser = TeamSerializer()

    class Meta:
        model = Match
        fields = "__all__"


class MatchPeriodSerializer(serializers.ModelSerializer):
    win_team = TeamSerializer()
    match = MatchSerializer()

    class Meta:
        model = MatchPeriod
        fields = "__all__"
