from rest_framework import serializers
from teams_and_players.models import Team, Player, CareerPeriod


class CareerPeriodSerializer(serializers.ModelSerializer):
    player = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="teams_and_players_app:player-detail"
    )
    team = serializers.StringRelatedField()

    class Meta:
        model = CareerPeriod
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    player_career = CareerPeriodSerializer(many=True)

    class Meta:
        model = Player
        fields = "__all__"
        depth = 1
