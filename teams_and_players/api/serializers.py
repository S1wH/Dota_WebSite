from rest_framework import serializers
from teams_and_players.models import Team, Player, CareerPeriod


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class CareerPeriodSerializer(serializers.ModelSerializer):
    player = serializers.HyperlinkedRelatedField(read_only=True,
                                                 view_name='teams_and_players_app:player-detail')
    team = serializers.HyperlinkedRelatedField(read_only=True,
                                               view_name='teams_and_players_app:team-detail')

    class Meta:
        model = CareerPeriod
        fields = '__all__'
