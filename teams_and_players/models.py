from django.db import models
from django.db.models import Sum, Count

# CONST
WIN_MATCHES = "win_matches"
LOSE_MATCHES = "lose_matches"
DRAW_MATCHES = "draw_matches"
PRIZE = "prize"


class MatchStatistic(models.Model):
    win_matches = models.IntegerField(default=0)
    lose_matches = models.IntegerField(default=0)
    draw_matches = models.IntegerField(default=0)
    prize = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Team(MatchStatistic):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    establish_date = models.DateField()
    logo = models.ImageField(upload_to="teams_logos")
    biography = models.TextField()

    def players_careers(self):
        current_players_careers = CareerPeriod.objects.filter(team=self, end_date=None)
        return current_players_careers

    def avg_age(self):
        all_players = Player.objects.filter(
            player_career__team=self, player_career__end_date=None
        )
        if all_players.exists():
            avg_age = round(
                all_players.aggregate(Sum("age"))["age__sum"]
                / all_players.aggregate(Count("id"))["id__count"],
                1,
            )
            return avg_age
        return 0

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=15)
    age = models.IntegerField()
    birthday = models.DateField()
    country = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="players_photos")
    biography = models.TextField()

    def team(self):
        return self.player_career.get(end_date=None).team

    def teammates(self):
        team = self.team()
        player_teammates = CareerPeriod.objects.filter(
            team=team, end_date=None
        ).exclude(player=self)
        return player_teammates

    def __str__(self):
        return self.nickname


class CareerPeriod(MatchStatistic):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_career"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_career")
    role = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.player} in {self.team} at period {self.start_date} - {self.end_date}"
