from django.test import TestCase
from mixer.backend.django import mixer
from teams_and_players.models import Team, Player, CareerPeriod
from users.models import MyUser


class TestTeamViews(TestCase):
    def test_list_get(self):
        response = self.client.get("/teams_and_players/teams/")
        self.assertEqual(response.status_code, 200)

    def test_detail_get(self):
        team = mixer.blend(Team)
        response = self.client.get(f"/teams_and_players/teams/{str(team.id)}/")
        self.assertEqual(response.status_code, 200)

    def test_create_get(self):
        url = f"/teams_and_players/teams/create/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "staff"
        password = "staff123"
        MyUser.objects.create_user(username, "staff@staff.com", password, is_staff=True)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_get(self):
        team = mixer.blend(Team)
        url = f"/teams_and_players/teams/update/{str(team.id)}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "staff"
        password = "staff123"
        email = "staff@staff.com"
        MyUser.objects.create_user(username, email, password, is_staff=True)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_get(self):
        team = mixer.blend(Team)
        url = f"/teams_and_players/teams/delete/{str(team.id)}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "admin"
        password = "admin123"
        email = "admin@admin.com"
        MyUser.objects.create_superuser(username, email, password)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_context_team(self):
        team = mixer.blend(Team, name="ABC", country="Russia")
        response = self.client.get(f"/teams_and_players/teams/{team.id}/")
        self.assertEqual(response.context["object"], team)

    def test_detail_context_country(self):
        team = mixer.blend(Team, name="ABC", country="Russia")
        response = self.client.get(f"/teams_and_players/teams/{team.id}/")
        self.assertEqual(response.context["object"].country, team.country)

    def test_detail_context_players(self):
        team = mixer.blend(Team, name="ABC", country="Russia")
        mixer.blend(CareerPeriod, team=team, end_date=None)
        mixer.blend(CareerPeriod, team=team, end_date=None)
        response = self.client.get(f"/teams_and_players/teams/{team.id}/")
        self.assertEqual(len(response.context["object"].players_careers()), 2)

    def test_create_content_button(self):
        username = "admin"
        email = "admin@admin.com"
        password = "admin123"
        MyUser.objects.create_superuser(username, email, password)
        self.client.login(username=username, password=password)
        response = self.client.get("/teams_and_players/teams/create/")
        submit_button = (
            '<input type="submit" value="Сохранить" class="btn btn-success">'
        )
        self.assertIn(submit_button, response.content.decode(encoding="utf-8"))


class TestPlayerViews(TestCase):
    def test_list_get(self):
        response = self.client.get("/teams_and_players/players/")
        self.assertEqual(response.status_code, 200)

    def test_detail_get(self):
        player = mixer.blend(Player)
        response = self.client.get(f"/teams_and_players/players/{str(player.id)}/")
        self.assertEqual(response.status_code, 200)

    def test_create_get(self):
        url = f"/teams_and_players/players/create/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "staff"
        password = "staff123"
        MyUser.objects.create_user(username, "staff@staff.com", password, is_staff=True)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_get(self):
        player = mixer.blend(Player)
        url = f"/teams_and_players/players/update/{str(player.id)}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "staff"
        password = "staff123"
        email = "staff@staff.com"
        MyUser.objects.create_user(username, email, password, is_staff=True)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_get(self):
        player = mixer.blend(Player)
        url = f"/teams_and_players/players/delete/{str(player.id)}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        username = "admin"
        password = "admin123"
        email = "admin@admin.com"
        MyUser.objects.create_superuser(username, email, password)
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_context_no_players(self):
        response = self.client.get("/teams_and_players/players/")
        self.assertIn("object_list", response.context)

    def test_list_context_some_players(self):
        mixer.blend(Player)
        mixer.blend(Player)
        response = self.client.get("/teams_and_players/players/")
        self.assertEqual(len(response.context["object_list"]), 2)

    def test_list_content_buttons(self):
        response = self.client.get("/teams_and_players/players/")
        teams_and_players_buttons = (
            '<div class="links" style="padding-top: 30px; max-width: 1200px; '
            'margin-left: auto; margin-right: auto;">'
        )
        self.assertIn(
            teams_and_players_buttons.encode(encoding="utf-8"), response.content
        )
