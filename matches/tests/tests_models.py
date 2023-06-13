from django.test import TestCase
from mixer.backend.django import mixer
from matches.models import Match, INCOMING, PLAYED, ONGOING, MatchPeriod, BO1
from datetime import timedelta
from teams_and_players.models import Team
from matches.errors import EmptyMatchPeriodError, PlayedMatchPeriodDeleteError


class TestMatch(TestCase):
    def test_create_incoming(self):
        match = mixer.blend(Match, status=INCOMING)
        self.assertEqual(match.status, INCOMING)

    def test_score_incoming(self):
        match = mixer.blend(Match, status=INCOMING)
        self.assertEqual(match.score(), "VS")

    def test_get_win_periods(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=PLAYED, team1=team1, team2=team2)
        mixer.cycle(4).blend(
            MatchPeriod, match=match, win_team=team1, duration=timedelta(minutes=40)
        )
        self.assertEqual(match.get_win_periods(team1), 4)

    def test_score_played(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=PLAYED, team1=team1, team2=team2)
        with self.assertRaises(EmptyMatchPeriodError):
            match.score()
        mixer.cycle(2).blend(
            MatchPeriod, match=match, win_team=team1, duration=timedelta(minutes=40)
        )
        mixer.blend(
            MatchPeriod, match=match, win_team=team2, duration=timedelta(minutes=40)
        )
        self.assertEqual(match.score(), "2:1")

    def test_score_ongoing(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=ONGOING, team1=team1, team2=team2)
        self.assertEqual(match.score(), "0:0")


class TestMatchPeriod(TestCase):
    def test_delete_not_played(self):
        match_period = mixer.blend(
            MatchPeriod, duration=timedelta(minutes=40), match__status=INCOMING
        )
        match_period.delete()
        self.assertFalse(MatchPeriod.objects.all().exists())

    # def test_delete_played(self):
    #     match = mixer.blend(Match, format=BO1)
    #     match_period = mixer.blend(MatchPeriod, duration=timedelta(minutes=40), match=match)
    #     with self.assertRaises(PlayedMatchPeriodDeleteError):
    #         match_period.delete()

    def test_delete_played_queryset(self):
        match = mixer.blend(Match, format=BO1)
        match_period = mixer.blend(
            MatchPeriod, duration=timedelta(minutes=40), match=match
        )
        MatchPeriod.not_played.all().delete()
        self.assertTrue(MatchPeriod.objects.filter(id=match_period.id).exists())

    def test_delete_played_queryset_delete(self):
        match = mixer.blend(Match, format=BO1)
        mixer.blend(MatchPeriod, duration=timedelta(minutes=40), match=match)
        with self.assertRaises(Exception):
            MatchPeriod.objects.all().delete()
