from django.db import models
from teams_and_players.models import Team, Player
from tournaments.models import TournamentStage
from matches.errors import EmptyMatchPeriodError

INCOMING = 'I'
ONGOING = 'O'
PLAYED = 'P'

BO1 = '1'
BO3 = '3'
BO5 = '5'

MATCH_PERIOD = 'MP'


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
    status = models.CharField(max_length=1, choices=statuses, default=INCOMING, editable=False)
    format = models.CharField(max_length=1, choices=formats, default=BO3)
    tournament_stage = models.ForeignKey(TournamentStage, on_delete=models.CASCADE,
                                         related_name='tournamentstage_matches')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        if self.id and kwargs['extra'] == MATCH_PERIOD:
            periods_played = self.match_period.all().count()
            if periods_played == int(self.format):
                self.status = PLAYED
            elif periods_played == 0:
                self.status = INCOMING
            else:
                self.status = ONGOING
        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)

    def get_win_periods(self, team):
        return self.match_period.filter(win_team=team).count()

    def score(self):
        if self.status == PLAYED and not self.match_period.all().exists():
            raise EmptyMatchPeriodError(self.id)
        if self.status == INCOMING:
            return 'VS'
        else:
            return f'{self.get_win_periods(self.team1)}:{self.get_win_periods(self.team2)}'

    def match_winner(self):
        return self.team1 if self.get_win_periods(self.team1) > self.get_win_periods(self.team2) else self.team2

    def match_loser(self):
        return self.team1 if self.get_win_periods(self.team1) < self.get_win_periods(self.team2) else self.team2

    def __str__(self):
        return f'Match between {self.team1} and {self.team2} on {self.tournament_stage}'


class NotPlayedMatchPeriodManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().exclude(match__status=PLAYED)


class MatchPeriodQuerySet(models.query.QuerySet):

    def delete(self):
        if self.filter(match__status=PLAYED).exists():
            raise Exception('Есть сыгранный матч, нельзя удалить выборку')
        return super().delete()


class MatchPeriodManager(models.Manager):

    def get_queryset(self):
        return MatchPeriodQuerySet(self.model, using=self._db)


class MatchPeriod(models.Model):
    objects = MatchPeriodManager()
    not_played = NotPlayedMatchPeriodManager()

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
