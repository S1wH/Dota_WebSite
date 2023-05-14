from django.test import TestCase
from mixer.backend.django import mixer
from tournaments.models import TournamentStage, Tournament
from teams_and_players.models import Team
from matches.models import Match, MatchPeriod, BO3, PLAYED
from datetime import timedelta
from tournaments.errors import NoPreviousStageError, WrongAmountTeamsError


class TestTournament(TestCase):
    def test_group_stage_table(self):
        teams = mixer.cycle(5).blend(Team)
        tournament = mixer.blend(Tournament, teams=teams)
        tournament_stage = mixer.blend(TournamentStage, stage=TournamentStage.GROUP_STAGE, tournament=tournament)
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                match = mixer.blend(Match, team1=teams[i], team2=teams[j],
                                    tournament_stage=tournament_stage, status=PLAYED, format=BO3)
                mixer.cycle(3).blend(MatchPeriod, win_team=match.team1, duration=timedelta(minutes=45), match=match)
        teams = {team: [4,
                        len(teams) - teams.index(team) - 1,
                        teams.index(team),
                        (len(teams) - teams.index(team) - 1) * 3]
                 for team in teams}
        self.assertEqual(tournament_stage.group_stage_table(), teams)

    def test_shuffle_teams(self):
        teams = mixer.cycle(5).blend(Team)
        tournament = mixer.blend(Tournament, teams=teams)
        group_stage = mixer.blend(TournamentStage, stage=TournamentStage.GROUP_STAGE, tournament=tournament)
        with self.assertRaises(NoPreviousStageError):
            group_stage.shuffle_teams()
        stage = mixer.blend(TournamentStage, stage=TournamentStage.ONE_EIGHT, tournament=tournament)
        with self.assertRaises(WrongAmountTeamsError):
            stage.shuffle_teams()
        team = mixer.blend(Team)
        teams.append(team)
        tournament.teams.add(team)
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                match = mixer.blend(Match, team1=teams[i], team2=teams[j],
                                    tournament_stage=group_stage, status=PLAYED, format=BO3)
                mixer.cycle(3).blend(MatchPeriod, win_team=match.team1, duration=timedelta(minutes=45), match=match)
        self.assertEqual(stage.shuffle_teams(), [(teams[0], teams[5]), (teams[1], teams[4]), (teams[2], teams[3])])

    def test_stage_winners(self):
        participants = mixer.cycle(16).blend(Team)
        tournament = mixer.blend(Tournament, teams=participants)
        group_stage = mixer.blend(TournamentStage, stage=TournamentStage.GROUP_STAGE, tournament=tournament)
        for i in range(len(participants)):
            for j in range(i + 1, len(participants)):
                match = mixer.blend(Match, team1=participants[i], team2=participants[j],
                                    tournament_stage=group_stage, status=PLAYED, format=BO3)
                mixer.cycle(3).blend(MatchPeriod, win_team=match.team1, duration=timedelta(minutes=45), match=match)

        one_eight = mixer.blend(TournamentStage, stage=TournamentStage.ONE_EIGHT, tournament=tournament)
        teams = one_eight.shuffle_teams()
        for pair in teams:
            team1, team2 = pair
            match = mixer.blend(Match, team1=team1, team2=team2,
                                tournament_stage=one_eight, status=PLAYED, format=BO3)
            mixer.cycle(3).blend(MatchPeriod, win_team=team1, duration=timedelta(minutes=45), match=match)
        self.assertEqual(one_eight.stage_winners(),
                         [participants[0], participants[1], participants[2], participants[3], participants[4],
                          participants[5], participants[6], participants[7]])

        quarter_finals = mixer.blend(TournamentStage, stage=TournamentStage.QUARTER_FINALS, tournament=tournament)
        teams = quarter_finals.shuffle_teams()
        for pair in teams:
            team1, team2 = pair
            match = mixer.blend(Match, team1=team1, team2=team2,
                                tournament_stage=quarter_finals, status=PLAYED, format=BO3)
            mixer.cycle(3).blend(MatchPeriod, win_team=team1, duration=timedelta(minutes=45), match=match)
        self.assertEqual(quarter_finals.stage_winners(),
                         [participants[0], participants[1], participants[2], participants[3]])

        semi_finals = mixer.blend(TournamentStage, stage=TournamentStage.SEMI_FINALS, tournament=tournament)
        teams = semi_finals.shuffle_teams()
        for pair in teams:
            team1, team2 = pair
            match = mixer.blend(Match, team1=team1, team2=team2,
                                tournament_stage=semi_finals, status=PLAYED, format=BO3)
            mixer.cycle(3).blend(MatchPeriod, win_team=team1, duration=timedelta(minutes=45), match=match)
        self.assertEqual(semi_finals.stage_winners(), [participants[0], participants[1]])

        final = mixer.blend(TournamentStage, stage=TournamentStage.FINAL, tournament=tournament)
        teams = final.shuffle_teams()
        team1, team2 = teams[0]
        match = mixer.blend(Match, team1=team1, team2=team2,
                            tournament_stage=final, status=PLAYED, format=BO3)
        mixer.cycle(3).blend(MatchPeriod, win_team=team2, duration=timedelta(minutes=45), match=match)
        self.assertEqual(*final.stage_winners(), participants[1])
