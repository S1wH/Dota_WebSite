from rest_framework.test import APITestCase, APIClient
from mixer.backend.django import mixer
from users.models import MyUser


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