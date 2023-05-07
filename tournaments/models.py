from django.db import models
from teams_and_players.models import Team


class Tournament(models.Model):
    name = models.CharField(max_length=30, unique=True)
    prize = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return f'{self.name} with prize {self.prize} at dates {self.start_date} -- {self.end_date}'


class TournamentStage(models.Model):
    GROUP_STAGE = 'GS'
    ONE_SIXTEEN = '1/16'
    ONE_EIGHT = '1/8'
    QUARTER_FINALS = '1/4'
    SEMI_FINALS = '1/2'
    FINAL = 'F'
    stages = (
        (GROUP_STAGE, 'Group Stage'),
        (ONE_SIXTEEN, '1/16'),
        (ONE_EIGHT, '1/8'),
        (QUARTER_FINALS, '1/4'),
        (SEMI_FINALS, '1/2'),
        (FINAL, 'Final'),
    )
    stage = models.CharField(max_length=20, choices=stages)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament_stages')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.stage} in {self.tournament}'
