from django.db import models
from django.db.models import Sum


class Team(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    establish_date = models.DateField()
    logo = models.ImageField(upload_to='teams_logos')
    biography = models.TextField()
    all_prize = models.IntegerField(default=0)
    all_win_matches = models.IntegerField(default=0)
    all_lose_matches = models.IntegerField(default=0)
    all_draw_matches = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Player(models.Model):
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=15)
    age = models.IntegerField()
    birthday = models.DateField()
    country = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='players_photos')
    biography = models.TextField()

    def team(self):
        return CareerPeriod.objects.get(player=self, end_date=None).team

    def prize(self):
        return self.sum_parameter_career_period('prize')

    def win_matches(self):
        return self.sum_parameter_career_period('win_matches')

    def lose_matches(self):
        return self.sum_parameter_career_period('lose_matches')

    def draw_matches(self):
        return self.sum_parameter_career_period('draw_matches')

    def sum_parameter_career_period(self, param):
        result = self.player_career.all().aggregate(Sum(param))[f'{param}__sum']
        return result
    def __str__(self):
        return f'name: {self.nickname}' # Player(name='Вася') -> должно в админке написано быть name: Вася


class CareerPeriod(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_career')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_career')
    role = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    prize = models.IntegerField(default=0)
    win_matches = models.IntegerField(default=0)
    lose_matches = models.IntegerField(default=0)
    draw_matches = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.player} in {self.team} at period {self.start_date} - {self.end_date}'
