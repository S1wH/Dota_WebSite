from datetime import timedelta
from django.test import TestCase
from mixer.backend.django import mixer
from tournaments.models import TournamentStage, Tournament
from tournaments.errors import WrongAmountTeamsError, NoNextStageError
from teams_and_players.models import Team
from matches.models import Match, MatchPeriod, BO3, PLAYED


class TestTournament(TestCase):
    def test_get_next_stage(self):
        tournament = mixer.blend(Tournament)
        group_stage = mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.GROUP_STAGE
        )
        one_eight = mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.ONE_EIGHT
        )
        self.assertEqual(group_stage.get_next_stage(), one_eight)
        quarter_finals = mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.QUARTER_FINALS
        )
        self.assertEqual(one_eight.get_next_stage(), quarter_finals)
        semi_finals = mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.SEMI_FINALS
        )
        self.assertEqual(quarter_finals.get_next_stage(), semi_finals)
        final = mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.FINAL
        )
        self.assertEqual(semi_finals.get_next_stage(), final)
        with self.assertRaises(NoNextStageError):
            final.get_next_stage()

    def test_group_stage_table(self):
        teams = mixer.cycle(6).blend(Team)
        tournament = mixer.blend(Tournament, teams=teams)
        group_stage = mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.GROUP_STAGE,
            teams=teams,
            group_table={},
        )
        mixer.blend(
            TournamentStage, tournament=tournament, stage=TournamentStage.ONE_EIGHT
        )
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                match = mixer.blend(
                    Match,
                    team1=teams[i],
                    team2=teams[j],
                    format=BO3,
                    status=PLAYED,
                    tournament_stage=group_stage,
                )
                mixer.cycle(3).blend(
                    MatchPeriod,
                    win_team=teams[i],
                    duration=timedelta(minutes=45),
                    match=match,
                )
        teams_dict = {
            teams[0]: [5, 15],
            teams[1]: [5, 12],
            teams[2]: [5, 9],
            teams[3]: [5, 6],
            teams[4]: [5, 3],
            teams[5]: [5, 0],
        }
        self.assertEqual(teams_dict, group_stage.group_stage_table())

    def test_shuffle_teams(self):
        teams = mixer.cycle(5).blend(Team)
        tournament = mixer.blend(Tournament, teams=teams)
        group_stage = mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.GROUP_STAGE,
            teams=teams,
        )
        one_eight = mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.ONE_EIGHT,
            teams=teams,
        )
        with self.assertRaises(WrongAmountTeamsError):
            one_eight.shuffle_teams()
        teams.append(mixer.blend(Team))
        group_stage.teams.add(teams[5])
        one_eight.teams.add(teams[5])
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                match = mixer.blend(
                    Match,
                    team1=teams[i],
                    team2=teams[j],
                    format=BO3,
                    status=PLAYED,
                    tournament_stage=group_stage,
                )
                mixer.cycle(3).blend(
                    MatchPeriod,
                    win_team=teams[i],
                    duration=timedelta(minutes=45),
                    match=match,
                )
        shuffled_teams = [
            (teams[0], teams[5]),
            (teams[1], teams[4]),
            (teams[2], teams[3]),
        ]
        self.assertEqual(shuffled_teams, one_eight.shuffle_teams())

    def test_stage_winners(self):
        teams = mixer.cycle(8).blend(Team)
        tournament = mixer.blend(Tournament, teams=teams)
        group_stage = mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.GROUP_STAGE,
            teams=teams,
            group_table={},
        )
        one_eight = mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.ONE_EIGHT,
        )
        mixer.blend(
            TournamentStage,
            tournament=tournament,
            stage=TournamentStage.QUARTER_FINALS,
        )
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                match = mixer.blend(
                    Match,
                    team1=teams[i],
                    team2=teams[j],
                    format=BO3,
                    status=PLAYED,
                    tournament_stage=group_stage,
                )
                mixer.cycle(3).blend(
                    MatchPeriod,
                    win_team=teams[i],
                    duration=timedelta(minutes=45),
                    match=match,
                )
        group_stage.group_stage_table()
        for pair in one_eight.shuffle_teams():
            team1, team2 = pair
            match = mixer.blend(
                Match,
                team1=team1,
                team2=team2,
                format=BO3,
                status=PLAYED,
                tournament_stage=one_eight,
            )
            mixer.cycle(3).blend(
                MatchPeriod, win_team=team1, duration=timedelta(minutes=45), match=match
            )
        winners = teams[0:4:]
        self.assertEqual(winners, one_eight.stage_winners())
