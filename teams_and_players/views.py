from django.shortcuts import render
from teams_and_players.models import Player, Team, CareerPeriod


def check_percentage(info: dict):
    if info['win_rate'] + info['lose_rate'] + info['draw_rate'] < 100:
        info['win_rate'] += 1
    elif info['win_rate'] + info['lose_rate'] + info['draw_rate'] > 100:
        info['win_rate'] -= 1


def teams_view(request):
    teams = Team.objects.all()
    all_teams_info = []

    for team in teams:
        info = {'id': team.id,
                'logo': team.logo,
                'name': team.name,
                'all_matches': team.all_win_matches + team.all_draw_matches + team.all_lose_matches,
                'all_win_matches': team.all_win_matches,
                'win_rate': round(team.all_win_matches / (
                        team.all_win_matches + team.all_draw_matches + team.all_lose_matches) * 100),
                'all_lose_matches': team.all_lose_matches,
                'lose_rate': round(team.all_lose_matches / (
                        team.all_win_matches + team.all_draw_matches + team.all_lose_matches) * 100),
                'all_draw_matches': team.all_draw_matches,
                'draw_rate': round(team.all_draw_matches / (
                        team.all_win_matches + team.all_draw_matches + team.all_lose_matches) * 100),
                'all_prize': team.all_prize,
                'establish_date': team.establish_date,
                }
        check_percentage(info)
        all_teams_info.append(info)
    return render(request, 'teams_and_players/teams.html', context={'teams': all_teams_info})


def players_view(request):
    players = Player.objects.all()
    all_players_info = []

    for player in players:
        all_career = player.player_career.all()
        win_matches = sum([item.win_matches for item in all_career])
        lose_matches = sum([item.lose_matches for item in all_career])
        draw_matches = sum([item.draw_matches for item in all_career])
        info = {'id': player.id,
                'photo': player.photo,
                'nickname': player.nickname,
                'name': player.name,
                'all_matches': win_matches + draw_matches + lose_matches,
                'all_win_matches': win_matches,
                'win_rate': round(win_matches / (win_matches + draw_matches + lose_matches) * 100),
                'all_lose_matches': lose_matches,
                'lose_rate': round(lose_matches / (win_matches + draw_matches + lose_matches) * 100),
                'all_draw_matches': draw_matches,
                'draw_rate': round(draw_matches / (win_matches + draw_matches + lose_matches) * 100),
                'all_prize': sum([item.prize for item in all_career]),
                'current_team': player.player_career.get(end_date=None).team,
                }
        print(player.player_career.get(end_date=None).team)
        check_percentage(info)
        all_players_info.append(info)
    return render(request, 'teams_and_players/players.html', context={'players': all_players_info})


def get_one_team_view(request, team_id):
    team = Team.objects.get(id=team_id)
    careers = CareerPeriod.objects.filter(team=team, end_date=None)
    players_info = []
    for player in careers:
        player_info = {
            'player': player.player,
            'role': player.role,
            'start_date': player.start_date,
            'all_matches': player.win_matches + player.draw_matches + player.lose_matches,
            'win_matches': player.win_matches,
            'win_rate': round(player.win_matches / (player.win_matches + player.draw_matches + player.lose_matches) * 100),
            'lose_matches': player.lose_matches,
            'lose_rate': round(player.lose_matches / (player.win_matches + player.draw_matches + player.lose_matches) * 100),
            'draw_matches': player.draw_matches,
            'draw_rate': round(player.draw_matches / (player.win_matches + player.draw_matches + player.lose_matches) * 100),
        }
        check_percentage(player_info)
        players_info.append(player_info)
    team_info = {'logo': team.logo,
                 'name': team.name,
                 'establish_date': team.establish_date,
                 'country': team.country,
                 'biography': team.biography,
                 'all_matches': team.all_win_matches + team.all_draw_matches + team.all_lose_matches,
                 'all_win_matches': team.all_win_matches,
                 'win_rate': round(team.all_win_matches / (team.all_win_matches + team.all_draw_matches +
                                                           team.all_lose_matches) * 100),
                 'all_lose_matches': team.all_lose_matches,
                 'lose_rate': round(team.all_lose_matches / (team.all_win_matches + team.all_draw_matches +
                                                             team.all_lose_matches) * 100),
                 'all_draw_matches': team.all_draw_matches,
                 'draw_rate': round(team.all_draw_matches / (team.all_win_matches + team.all_draw_matches +
                                                             team.all_lose_matches) * 100),
                 'all_prize': team.all_prize,
                 'avg_age': round(sum([player.player.age for player in careers]) / len(players_info)
                                  if len(players_info) > 0 else 0, 1),
                 }
    check_percentage(team_info)
    return render(request, 'teams_and_players/one_team.html', context={'team': team_info, 'players': players_info})


def get_one_player_view(request, player_id):
    player = Player.objects.get(id=player_id)
    career_periods = CareerPeriod.objects.filter(player=player)
    player_info = {
        'name': player.name,
        'nickname': player.nickname,
        'age': player.age,
        'birthday': player.birthday,
        'biography': player.biography,
        'country': player.country,
        'photo': player.photo,
        'team': CareerPeriod.objects.get(player=player, end_date=None).team,
        'prize': sum([career.prize for career in career_periods]),
        'win_matches': sum([career.win_matches for career in career_periods]),
        'lose_matches': sum([career.lose_matches for career in career_periods]),
        'draw_matches': sum([career.draw_matches for career in career_periods]),
    }
    player_info['all_matches'] = player_info['win_matches'] + player_info['lose_matches'] + player_info['draw_matches']
    player_info['win_rate'] = round(player_info['win_matches'] / player_info['all_matches'] * 100)
    player_info['lose_rate'] = round(player_info['lose_matches'] / player_info['all_matches'] * 100)
    player_info['draw_rate'] = round(player_info['draw_matches'] / player_info['all_matches'] * 100)
    print(player_info['all_matches'])
    check_percentage(player_info)
    player_teammates = CareerPeriod.objects.filter(team=player_info['team'], end_date=None).exclude(player=player)
    teammates = []
    for teammate in player_teammates:

        player_teammate_info = {
            'photo': teammate.player.photo,
            'nickname': teammate.player.nickname,
        }
        teammates.append(player_teammate_info)
    return render(request, 'teams_and_players/one_player.html', context={'player': player_info, 'teammates': teammates})
