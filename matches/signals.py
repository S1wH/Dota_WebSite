from django.db.models.signals import post_save
from django.dispatch import receiver
from matches.models import MatchPeriod, Match, MATCH_PERIOD, PLAYED
from tournaments.models import TournamentStage


@receiver(post_save, sender=MatchPeriod)
def match_period_post_save(**kwargs):
    if kwargs["update_fields"] is None:
        match_period = kwargs["instance"]
        match_period.match.save(extra=MATCH_PERIOD)


@receiver(post_save, sender=Match)
def match_post_save(**kwargs):
    match = kwargs["instance"]
    tournament_stage = match.tournament_stage
    if match.status == PLAYED and tournament_stage.stage == TournamentStage.GROUP_STAGE:
        if match.winner is not None and match.loser is not None:
            winner = match.winner.id
            loser = match.loser.id
            group_table = tournament_stage.group_table
            if winner in group_table.keys():
                group_table[winner][0] += 1
                group_table[winner][1] += 3
            else:
                group_table[winner] = [1, 3]
            if loser in group_table.keys():
                group_table[loser][0] += 1
            else:
                group_table[loser] = [1, 0]
            match.tournament_stage.group_table = group_table
            match.tournament_stage.save()
