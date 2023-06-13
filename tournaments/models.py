from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from teams_and_players.models import Team
from tournaments.errors import WrongAmountTeamsError, NoPreviousStageError
from matches.errors import MatchNotfound


class Tournament(models.Model):
    name = models.CharField(max_length=30, unique=True)
    prize = models.IntegerField(default=0)
    place = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField(Team)

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
    start_date = models.DateField()
    end_date = models.DateField()

    def group_stage_table(self):
        # matches, wins, loses, points
        matches = self.tournamentstage_matches.all()
        teams = {team: [0, 0, 0, 0] for team in self.tournament.teams.all()}
        for match in matches:
            winner = match.match_winner()
            loser = match.match_loser()
            teams[winner][0] += 1
            teams[loser][0] += 1
            teams[winner][1] += 1
            teams[loser][2] += 1
            teams[winner][3] += 3
        return dict(sorted(teams.items(), key=lambda x: x[1], reverse=True))

    def get_previous_stage(self):
        if self.stage == self.GROUP_STAGE:
            raise NoPreviousStageError(self)
        if self.stage == self.ONE_EIGHT:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.GROUP_STAGE
            )
        if self.stage == self.QUARTER_FINALS:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.ONE_EIGHT
            )
        if self.stage == self.SEMI_FINALS:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.QUARTER_FINALS
            )
        if self.stage == self.FINAL:
            return self.tournament.tournament_stages.get(
                stage=TournamentStage.SEMI_FINALS
            )

    def shuffle_teams(self):
        prev_stage = self.get_previous_stage()
        if self.stage == self.ONE_EIGHT:
            teams = list(prev_stage.group_stage_table().keys())
        else:
            teams = list(prev_stage.stage_winners())
        length = len(teams)
        if length % 2 != 0:
            raise WrongAmountTeamsError(self)
        return [list(zip(teams[:length // 2], teams[-1:-length // 2 - 1:-1]))]

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
            winners.append(match.match_winner())
        return winners

    def __str__(self):
        return f"{self.stage} in {self.tournament}"
