from django.db import models
from teams_and_players.models import Team, Player
from tournaments.models import TournamentStage

INCOMING = 'I'
ONGOING = 'O'
PLAYED = 'P'

BO1 = '1'
BO3 = '3'
BO5 = '5'


class Match(models.Model):
    statuses = (
        (INCOMING, 'Incoming'),
        (ONGOING, 'Ongoing'),
        (PLAYED, 'Played'),
    )
    formats = (
        (BO1, 'BO1'),
        (BO3, 'BO3'),
        (BO5, 'BO5'),
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_match')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_match')
    status = models.CharField(max_length=1, choices=statuses, default=INCOMING)
    format = models.CharField(max_length=1, choices=formats, default=BO3)
    tournament_stage = models.ForeignKey(TournamentStage, on_delete=models.CASCADE,
                                         related_name='tournamentstage_matches')

    def __str__(self):
        return f'Match between {self.team1} and {self.team2}'


class MatchPeriod(models.Model):
    win_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_period_win')
    duration = models.DurationField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_period')

    def __str__(self):
        return f'period in match {self.match}, win team is {self.win_team}'


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
