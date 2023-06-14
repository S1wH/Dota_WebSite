from django.db.models.signals import post_save
from django.dispatch import receiver
from matches.models import MatchPeriod, MATCH_PERIOD


# from matches.errors import PlayedMatchPeriodDeleteError


@receiver(post_save, sender=MatchPeriod)
def match_period_post_save(**kwargs):
    if kwargs["update_fields"] is None:
        match_period = kwargs["instance"]
        match_period.match.save(extra=MATCH_PERIOD)

# @receiver(pre_delete, sender=MatchPeriod)
# def match_period_pre_delete(**kwargs):
#     match_period = kwargs['instance']
#     if match_period.match.status == PLAYED:
#         raise PlayedMatchPeriodDeleteError(match_period)
