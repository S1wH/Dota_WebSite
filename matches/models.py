from django.db import models
from teams_and_players.models import Team, Player


class Match(models.Model):
    start_date = models.DateTimeField()

    class Meta:
        abstract = True


class PlayedMatch(Match):
    end_date = models.DateTimeField()


class IncomingMatch(Match):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_incoming_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_incoming_match')


class OnGoingMatch(Match):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_incoming_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_incoming_match')


class MatchPeriod(models.Model):
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_period_win')
    lose_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='lose_period_win')
    duration = models.DurationField()
    match = models.ForeignKey()


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
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='player_stats')
