from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from mixer.backend.django import mixer
from tournaments.models import Tournament, TournamentStage


class TestTournamentView(TestCase):
    def test_current_list_get(self):
        response = self.client.get("/tournaments/current_tournaments/")
        self.assertEqual(response.status_code, 200)

    def test_previous_list_get(self):
        response = self.client.get("/tournaments/previous_tournaments/")
        self.assertEqual(response.status_code, 200)

    def test_future_list_get(self):
        response = self.client.get("/tournaments/future_tournaments/")
        self.assertEqual(response.status_code, 200)

    def test_detail_get(self):
        tournament = mixer.blend(Tournament)
        response = self.client.get(f"/tournaments/{tournament.id}/")
        self.assertEqual(response.status_code, 200)

    def test_current_list_content(self):
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=5),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=2),
            end_date=timezone.now() + timedelta(days=10),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=3),
            end_date=timezone.now() + timedelta(days=15),
        )
        response = self.client.get("/tournaments/current_tournaments/")
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_future_list_content(self):
        mixer.blend(
            Tournament,
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=5),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() + timedelta(days=2),
            end_date=timezone.now() + timedelta(days=10),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() + timedelta(days=3),
            end_date=timezone.now() + timedelta(days=15),
        )
        response = self.client.get("/tournaments/future_tournaments/")
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_previous_list_content(self):
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=10),
            end_date=timezone.now() - timedelta(days=5),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=20),
            end_date=timezone.now() - timedelta(days=10),
        )
        mixer.blend(
            Tournament,
            start_date=timezone.now() - timedelta(days=30),
            end_date=timezone.now() - timedelta(days=15),
        )
        response = self.client.get("/tournaments/previous_tournaments/")
        self.assertEqual(len(response.context["object_list"]), 3)

    def test_detail_context(self):
        tournament = mixer.blend(Tournament)
        mixer.blend(TournamentStage, stage="Group Stage", tournament=tournament)
        mixer.blend(TournamentStage, stage="Final", tournament=tournament)
        response = self.client.get(f"/tournaments/{tournament.id}/")
        self.assertEqual(len(response.context["object"].tournament_stages.all()), 2)
