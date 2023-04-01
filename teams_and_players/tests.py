from django.test import TestCase
from mixer.backend.django import mixer
from .models import Player, Team, CareerPeriod


class TestPlayer(TestCase):

    def test_team(self):
        team = mixer.blend(Team)
        player = mixer.blend(Player)
        mixer.blend(CareerPeriod, team=team, player=player, end_date=None)
        self.assertEqual(player.team().id, team.id)

    def test_sum_parameter_career_period(self):
        param = 'win_matches'
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=345)
        self.assertEqual(player.sum_parameter_career_period(param), career_1.win_matches + career_2.win_matches)

    def test_prize(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, prize=213)
        career_2 = mixer.blend(CareerPeriod, player=player, prize=345)
        self.assertEqual(player.prize(), career_1.prize + career_2.prize)

    def test_win_matches(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=345)
        self.assertEqual(player.win_matches(), career_1.win_matches + career_2.win_matches)

    def test_lose_matches(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, lose_matches=213)
        career_2 = mixer.blend(CareerPeriod, player=player, lose_matches=345)
        self.assertEqual(player.lose_matches(), career_1.lose_matches + career_2.lose_matches)

    def test_draw_matches(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, draw_matches=213)
        career_2 = mixer.blend(CareerPeriod, player=player, draw_matches=345)
        self.assertEqual(player.draw_matches(), career_1.draw_matches + career_2.draw_matches)

    def test_all_matches(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213, lose_matches=12, draw_matches=324)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=203, lose_matches=132, draw_matches=32)
        self.assertEqual(player.all_matches(), career_1.win_matches + career_1.lose_matches + career_1.draw_matches
                         + career_2.win_matches + career_2.lose_matches + career_2.draw_matches)

    def test_rate(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213, lose_matches=12, draw_matches=324)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=203, lose_matches=132, draw_matches=32)
        param = player.win_matches()
        self.assertEqual(player.rate(param), round((career_1.win_matches + career_2.win_matches) /
                                                   (career_1.win_matches + career_1.lose_matches + career_1.draw_matches
                                                    + career_2.win_matches + career_2.lose_matches
                                                    + career_2.draw_matches) * 100))

    def test_win_rate(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213, lose_matches=12, draw_matches=324)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=203, lose_matches=132, draw_matches=32)
        self.assertEqual(player.win_rate(), round((career_1.win_matches + career_2.win_matches) /
                                                   (career_1.win_matches + career_1.lose_matches + career_1.draw_matches
                                                    + career_2.win_matches + career_2.lose_matches
                                                    + career_2.draw_matches) * 100))

    def test_lose_rate(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213, lose_matches=12, draw_matches=324)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=203, lose_matches=132, draw_matches=32)
        self.assertEqual(player.lose_rate(), round((career_1.lose_matches + career_2.lose_matches) /
                                                   (career_1.win_matches + career_1.lose_matches + career_1.draw_matches
                                                    + career_2.win_matches + career_2.lose_matches
                                                    + career_2.draw_matches) * 100))

    def test_draw_rate(self):
        player = mixer.blend(Player)
        career_1 = mixer.blend(CareerPeriod, player=player, win_matches=213, lose_matches=12, draw_matches=324)
        career_2 = mixer.blend(CareerPeriod, player=player, win_matches=203, lose_matches=132, draw_matches=32)
        self.assertEqual(player.draw_rate(), round((career_1.draw_matches + career_2.draw_matches) /
                                                   (career_1.win_matches + career_1.lose_matches + career_1.draw_matches
                                                    + career_2.win_matches + career_2.lose_matches
                                                    + career_2.draw_matches) * 100))

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
        self.assertEqual([career for career in team.players_careers()], [career1, career2])

    def test_avg_age(self):
        team = mixer.blend(Team)
        player1 = mixer.blend(Player)
        player2 = mixer.blend(Player)
        mixer.blend(CareerPeriod, player=player1, team=team, end_date=None)
        mixer.blend(CareerPeriod, player=player2, team=team, end_date=None)
        self.assertEqual(team.avg_age(), round((player1.age + player2.age) / 2, 1))
