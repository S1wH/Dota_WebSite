from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from mixer.backend.django import mixer
from users.models import MyUser
from matches.models import Match, MatchPeriod
from teams_and_players.models import Team


class TestMatches(APITestCase):

    def setUp(self):
        self.url = '/matches/api/matches/'
        self.auth_client = APIClient()
        user = mixer.blend(MyUser)
        self.auth_client.force_authenticate(user=user)

    def test_status_code_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_status_code_auth(self):
        response = self.auth_client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestMatchPeriod(APITestCase):

    def setUp(self):
        self.url = '/matches/api/match_periods/'
        self.auth_client = APIClient()
        user = mixer.blend(MyUser)
        self.auth_client.force_authenticate(user=user)

    def test_status_code_guest(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_status_code_auth(self):
        response = self.auth_client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        match = mixer.blend(Match)
        team = mixer.blend(Team)
        response = self.auth_client.post(self.url,
                                         {
                                             'duration': timedelta(minutes=45),
                                             'win_team': team.id,
                                             'match': match.id,
                                         })
        self.assertEqual(response.status_code, 201)

    def test_put(self):
        match_period = mixer.blend(MatchPeriod, duration=timedelta(30))
        url = self.url + f'{match_period.id}/'
        match = mixer.blend(Match)
        team = mixer.blend(Team)
        response = self.auth_client.put(url,
                                        {
                                            'duration': timedelta(minutes=35),
                                            'win_team': team.id,
                                            'match': match.id,
                                        })
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        match_period = mixer.blend(MatchPeriod, duration=timedelta(30))
        url = self.url + f'{match_period.id}/'
        response = self.auth_client.delete(url)
        self.assertEqual(response.status_code, 204)
