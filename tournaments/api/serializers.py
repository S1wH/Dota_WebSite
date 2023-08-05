from rest_framework import serializers
from tournaments.models import Tournament, TournamentStage


class TournamentSerializer(serializers.ModelSerializer):
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tournament
        fields = "__all__"


class TournamentStageSerializer(serializers.ModelSerializer):
    tournament = serializers.StringRelatedField()
    teams = serializers.StringRelatedField(many=True)

    class Meta:
        model = TournamentStage
        fields = "__all__"
