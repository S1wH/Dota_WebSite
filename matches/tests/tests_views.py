from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer
from matches.models import Match, MatchPeriod
from datetime import timedelta


class TestMatchView(TestCase):

    def test_ongoing_list_get(self):
        response = self.client.get('/matches/ongoing_matches/')
        self.assertEqual(response.status_code, 200)

    def test_incoming_list_get(self):
        response = self.client.get('/matches/incoming_matches/')
        self.assertEqual(response.status_code, 200)

    def test_played_list_get(self):
        response = self.client.get('/matches/played_matches/')
        self.assertEqual(response.status_code, 200)

    def test_ongoing_list_content(self):
        mixer.blend(Match, start_date=timezone.now() + timedelta(hours=2),
                    end_date=timezone.now() + timedelta(hours=30))
        mixer.blend(Match, start_date=timezone.now() - timedelta(minutes=10),
                    end_date=None)
        mixer.blend(Match, start_date=timezone.now() - timedelta(minutes=15),
                    end_date=None)
        response = self.client.get('/matches/ongoing_matches/')
        self.assertEqual(len(response.context['object_list']), 2)

    def test_incoming_list_content(self):
        mixer.blend(Match, start_date=timezone.now() + timedelta(days=3),
                    end_date=None)
        mixer.blend(Match, start_date=timezone.now() - timedelta(minutes=10),
                    end_date=None)
        mixer.blend(Match, start_date=timezone.now() + timedelta(minutes=35),
                    end_date=None)
        response = self.client.get('/matches/incoming_matches/')
        self.assertEqual(len(response.context['object_list']), 2)

    def test_played_list_content(self):
        mixer.blend(Match, start_date=timezone.now() - timedelta(days=3),
                    end_date=timezone.now() - timedelta(hours=14))
        mixer.blend(Match, start_date=timezone.now() - timedelta(minutes=30),
                    end_date=None)
        mixer.blend(Match, start_date=timezone.now() + timedelta(minutes=35),
                    end_date=timezone.now() + timedelta(hours=4))
        response = self.client.get('/matches/played_matches/')
        self.assertEqual(len(response.context['object_list']), 1)

