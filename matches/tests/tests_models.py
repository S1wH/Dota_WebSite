from django.test import TestCase
from mixer.backend.django import mixer
from matches.models import Match, INCOMING, PLAYED, ONGOING, MatchPeriod
from datetime import timedelta
from teams_and_players.models import Team
from matches.errors import EmptyMatchPeriodError


class TestMatch(TestCase):

    def test_score_incoming(self):
        match = mixer.blend(Match, status=INCOMING)
        self.assertEqual(match.score(), 'VS')

    def test_get_win_periods(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=PLAYED, team1=team1, team2=team2)
        mixer.cycle(4).blend(MatchPeriod, match=match, win_team=team1, duration=timedelta(minutes=40))
        self.assertEqual(match.get_win_periods(team1), 4)

    def test_score_played(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=PLAYED, team1=team1, team2=team2)
        with self.assertRaises(EmptyMatchPeriodError):
            match.score()
        mixer.cycle(2).blend(MatchPeriod, match=match, win_team=team1, duration=timedelta(minutes=40))
        mixer.blend(MatchPeriod, match=match, win_team=team2, duration=timedelta(minutes=40))
        self.assertEqual(match.score(), '2:1')

    def test_score_ongoing(self):
        team1 = mixer.blend(Team)
        team2 = mixer.blend(Team)
        match = mixer.blend(Match, status=ONGOING, team1=team1, team2=team2)
        self.assertEqual(match.score(), '0:0')
