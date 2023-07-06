from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from teams_and_players.models import Team
from tournaments.errors import WrongAmountTeamsError, NoNextStageError
from matches.errors import MatchNotfound


class Tournament(models.Model):
    name = models.CharField(max_length=30, unique=True)
    prize = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField(Team, related_name="tournaments")

    def __str__(self):
        return f"{self.name} with prize {self.prize} at dates {self.start_date} -- {self.end_date}"


class TournamentStage(models.Model):
    GROUP_STAGE = "GS"
    ONE_EIGHT = "1/8"
    QUARTER_FINALS = "1/4"
    SEMI_FINALS = "1/2"
    FINAL = "F"
    stages = (
        (GROUP_STAGE, "Group Stage"),
        (ONE_EIGHT, "1/8"),
        (QUARTER_FINALS, "1/4"),
        (SEMI_FINALS, "1/2"),
        (FINAL, "Final"),
    )

    stage = models.CharField(max_length=20, choices=stages)
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="tournament_stages"
    )
    teams = models.ManyToManyField(Team, related_name="tournaments_stages")
    start_date = models.DateField()
    end_date = models.DateField()
    group_table = models.JSONField(default=dict(), blank=True, null=True)

    def group_stage_table(self):
        no_add = False
        d = {}
        teams_dict = self.group_table
        amount_teams = self.teams.all().count() - 1
        for team, scores in teams_dict.items():
            if scores[0] != amount_teams:
                no_add = True
                break
        if not no_add:
            next_stage = self.get_next_stage()
            for team_id, team_stats in teams_dict.items():
                team = Team.objects.get(id=team_id)
                next_stage.teams.add(team)
                d[team] = team_stats
        return dict(sorted(d.items(), key=lambda x: x[1], reverse=True))

    def get_next_stage(self):
        if self.stage == self.GROUP_STAGE:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.ONE_EIGHT
            )
        if self.stage == self.ONE_EIGHT:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.QUARTER_FINALS
            )
        if self.stage == self.QUARTER_FINALS:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.SEMI_FINALS
            )
        if self.stage == self.SEMI_FINALS:
            return self.tournament.tournament_stages.get(stage=TournamentStage.FINAL)
        if self.stage == self.FINAL:
            raise NoNextStageError(self)

    def shuffle_teams(self):
        if self.stage != self.GROUP_STAGE:
            teams = self.teams.all()
            length = teams.count()
            if length % 2 != 0:
                raise WrongAmountTeamsError(self.stage)
            return list(
                zip(teams[: length // 2], teams.order_by("-id")[: length // 2 :])
            )

    def stage_winners(self):
        winners = []
        for pair in self.shuffle_teams():
            team1, team2 = pair
            try:
                match = self.tournamentstage_matches.get(team1=team1, team2=team2)
            except ObjectDoesNotExist:
                try:
                    match = self.tournamentstage_matches.get(team1=team2, team2=team1)
                except ObjectDoesNotExist as e:
                    raise MatchNotfound(team1, team2, self) from e
            winners.append(match.winner)
        if self.stage != self.FINAL:
            next_stage = self.get_next_stage()
            for team in winners:
                next_stage.teams.add(team)
        return winners

    # def __str__(self):
    #     return f"{self.stage} in {self.tournament}"
