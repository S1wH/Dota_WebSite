from django.test import TestCase
from mixer.backend.django import mixer
from .models import Player, Team, CareerPeriod


class TestPlayer(TestCase):

    def test_team(self):
        team = mixer.blend(Team)
        player = mixer.blend(Player)
        mixer.blend(CareerPeriod, team=team, player=player, end_date=None)
        self.assertEqual(player.team().id, team.id)