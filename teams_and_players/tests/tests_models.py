from django.test import TestCase
from mixer.backend.django import mixer
from teams_and_players.models import Player, Team, CareerPeriod


class TestPlayer(TestCase):
    def test_team(self):
        team = mixer.blend(Team)
        player = mixer.blend(Player)
        mixer.blend(CareerPeriod, team=team, player=player, end_date=None)
        self.assertEqual(player.team().id, team.id)

    def test_teammates(self):
        team = mixer.blend(Team)
        player = mixer.blend(Player)
        teammate1 = mixer.blend(Player)
        teammate2 = mixer.blend(Player)
        mixer.blend(CareerPeriod, player=player, team=team, end_date=None)
        career1 = mixer.blend(CareerPeriod, player=teammate1, team=team, end_date=None)
        career2 = mixer.blend(CareerPeriod, player=teammate2, team=team, end_date=None)
        self.assertEqual([player for player in player.teammates()], [career1, career2])


class TestTeam(TestCase):
    def test_players_careers(self):
        team = mixer.blend(Team)
        player1 = mixer.blend(Player)
        player2 = mixer.blend(Player)
        career1 = mixer.blend(CareerPeriod, player=player1, team=team, end_date=None)
        career2 = mixer.blend(CareerPeriod, player=player2, team=team, end_date=None)
        self.assertEqual(
            [career for career in team.players_careers()], [career1, career2]
        )

    def test_avg_age(self):
        team = mixer.blend(Team)
        player1 = mixer.blend(Player)
        player2 = mixer.blend(Player)
        mixer.blend(CareerPeriod, player=player1, team=team, end_date=None)
        mixer.blend(CareerPeriod, player=player2, team=team, end_date=None)
        self.assertEqual(team.avg_age(), round((player1.age + player2.age) / 2, 1))
