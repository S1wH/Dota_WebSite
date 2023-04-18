from django.db import models
from teams_and_players.models import Team, Player

INCOMING = 'Incoming'
ONGOING = 'Ongoing'
PLAYED = 'Played'

BO1 = 'bo1'
BO3 = 'bo3'
BO5 = 'bo5'


class Match(models.Model):
    statuses = [
        (1, INCOMING),
        (2, ONGOING),
        (3, PLAYED),
    ]
    formats = [
        (1, BO1),
        (2, BO3),
        (3, BO5),
    ]
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_match')
    status = models.CharField(max_length=10, choices=statuses, default=1)
    format = models.CharField(max_length=3, choices=formats, default=2)

    # TODO: tournament foreign key


class MatchPeriod(models.Model):
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_period_win')
    duration = models.DurationField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_period')


class PlayerStats(models.Model):
    kills_amount = models.IntegerField(default=0)
    deaths_amount = models.IntegerField(default=0)
    assist_amount = models.IntegerField(default=0)
    damage_dealt = models.IntegerField(default=0)
    damage_received = models.IntegerField(default=0)
    heal_amount = models.IntegerField(default=0)
    money_earned = models.IntegerField(default=0)
    support_money_spent = models.IntegerField(default=0)
    match_period = models.ForeignKey(MatchPeriod, on_delete=models.CASCADE, related_name='period_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_stats')
