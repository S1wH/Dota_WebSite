from rest_framework import serializers
from matches.models import Match, MatchPeriod


class MatchSerializer(serializers.ModelSerializer):
    team1 = serializers.StringRelatedField()
    team2 = serializers.StringRelatedField()
    winner = serializers.StringRelatedField()
    loser = serializers.StringRelatedField()
    tournament_stage = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = "__all__"


class MatchPeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchPeriod
        fields = "__all__"
