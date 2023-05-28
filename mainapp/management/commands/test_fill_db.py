from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from news.models import News, Author, Image
from teams_and_players.models import Team, Player, CareerPeriod
from tournaments.models import Tournament, TournamentStage
from matches.models import Match, MatchPeriod, BO1, BO3, BO5, PLAYED
from django.core.files.images import ImageFile
from random import choice, randint
from datetime import timedelta
import os
from django.conf import settings


def create_match(stage, team1, team2, formats, matches, matches_periods):
    match = Match(start_date=stage.start_date,
                  end_date=stage.start_date + timedelta(minutes=40),
                  team1=team1,
                  team2=team2,
                  status=PLAYED,
                  tournament_stage=stage,
                  format=choice(formats))
    for k in range(int(match.format)):
        match_period = MatchPeriod(win_team=choice([match.team1, match.team2]),
                                   duration=timedelta(minutes=45),
                                   match=match)
        matches_periods.append(match_period)
    matches.append(match)
    print(match)


def create_matches(stage, formats, matches, matches_periods):
    teams = stage.shuffle_teams()
    for pair in teams:
        team1, team2 = pair
        create_match(stage, team1, team2, formats, matches, matches_periods)


class Command(BaseCommand):
    help = 'Filling database with test data'

    def handle(self, *args, **options):
        # Delete all previous data
        Author.objects.all().delete()
        News.objects.all().delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        CareerPeriod.objects.all().delete()
        Tournament.objects.all().delete()
        TournamentStage.objects.all().delete()
        MatchPeriod.objects.all().delete()
        Match.objects.all().delete()

        # Creating authors
        print('Creating authors...\n')
        author_nicknames = [
            'Paul',
            'Andrew',
            'Nikolai',
            'Gleb',
            'Slava',
        ]
        authors = []
        for i in range(len(author_nicknames)):
            author = Author(
                nickname=author_nicknames[i],
                rating=i + 1
            )
            authors.append(author)
            print(author)
        Author.objects.bulk_create(authors)
        print('\nall authors successfully created\n')

        # Creating news
        print('Creating news...\n')
        news = []
        for i in range(11):
            one_news = News(
                header=f'News №{i + 1}',
                summary=f'This is a brief summary of a news with a header News №{i + 1}',
                text=f'Here should be a really long text about news with a header News №{i + 1}, but I am kinda lazy.\n'
                     'Although this text makes sense. I am glad to write it, because I do it instead of listening '
                     'to my Physics teacher',
                author=choice(authors),
                publish_date=timezone.now(),
                importance_index=True if i < 9 else False,
            )
            path = os.path.join(settings.BASE_DIR, f'static/photos/dota/news{i + 1}.jpg')
            one_news.main_image = ImageFile(open(path, 'rb'), name=f'news{i + 1}.jpg')
            print(one_news, one_news.publish_date)
            news.append(one_news)
        News.objects.bulk_create(news)
        print('\nAll news successfully created\n')

        # Creating Images for news
        print('Creating images for news...\n')
        images = []
        for item in news:
            for i in range(3):
                image = Image(
                    title=f'title {i} for {item}',
                    image=ImageFile(open(f'one_news.jpg', 'rb')),
                    news_id=item,
                )
                print(image)
                images.append(image)
        Image.objects.bulk_create(images)
        print('\nAll images successfully created\n')

        # Creating teams
        print('Creating teams...\n')
        teams = []
        teams_names = [
            'team Spirit',
            'team Liquid',
            'PSG.LGD',
            'team Secret',
            "Na'Vi",
            'BetBoom',
            'Nemiga',
            'One Move',
            'VP',
            'Entity',
            'OG',
            'Evil Geniuses',
            'Gladiators',
            'Thunder',
            'BOOM',
            'Aster'
        ]
        countries = ['Russia', 'US', 'Germany', 'Brazil', 'Spain', 'UK']

        for i in range(16):
            team = Team(
                name=teams_names[i],
                country=choice(countries),
                establish_date='2003-12-23',
                biography=f'{teams_names[i]} is a really great team. '
                          f'It was performing wonderfully',
                prize=randint(1000000, 15000000),
                win_matches=randint(1000, 2000),
                lose_matches=randint(500, 1200),
                draw_matches=randint(10, 100),
            )
            path = os.path.join(settings.BASE_DIR, f'static/photos/team{i + 1}.jpg')
            team.logo = ImageFile(open(path, 'rb'), name=f'team{i + 1}.jpg')
            print(team)
            teams.append(team)
        Team.objects.bulk_create(teams)
        print('\nAll teams successfully created\n')

        # Creating players
        print('Creating players...\n')
        players = []
        names = [
            'Paul',
            'Topias',
            'Kirill',
            'Chua',
            'Oleg',
        ]
        nicknames = [
            'S1wH',
            'Topson',
            'Miposhka',
            'Faith_Bian',
            'Yatoro',
        ]
        for i in range(5):
            player = Player(
                name=names[i],
                nickname=nicknames[i],
                age=randint(18, 30),
                birthday='2003-12-23',
                country=choice(countries),
                biography='This player is great. I am serious.'
                          'He won a lot of trophies and made all his '
                          'teams great once again.'
            )
            path = os.path.join(settings.BASE_DIR, 'static/photos/player.jpg')
            player.photo = ImageFile(open(path, 'rb'), name=f'player{i + 1}.jpg')
            print(player)
            players.append(player)
        Player.objects.bulk_create(players)
        print('\nall players successfully created\n')

        # Creating Career Histories
        print('Creating career periods...\n')
        roles = ['support', 'carry', 'semi-support', 'off-lane', 'mid-lane']
        dates = ['2017-12-23', '2019-05-27', '2020-04-16', '2021-09-13', None]
        periods = []

        for player in players:
            for i in range(4):
                period = CareerPeriod(
                    player=player,
                    team=choice(teams),
                    role=choice(roles),
                    start_date=dates[i],
                    end_date=dates[i + 1],
                    prize=randint(5000, 1000000),
                    win_matches=randint(10, 200),
                    lose_matches=randint(10, 200),
                    draw_matches=randint(1, 30),
                )
                print(period)
                periods.append(period)
        CareerPeriod.objects.bulk_create(periods)
        print('\nall career periods successfully created\n')

        # Creating Tournaments
        print('Creating tournaments...\n')
        tournaments = []
        names_previous = ['ESL COLOGNE 2023', 'Paris Major 2023', 'DPC League season 13']
        names_current = ['ESL Antwerpen 2023', 'Moscow Major 2023', 'DPC League season 14']
        names_future = ['ESL Katowice 2023', 'Bali Major 2023', 'DPC League season 15']
        places_previous = ['Cologne', 'Paris', 'Online']
        places_current = ['Antwerpen', 'Moscow', 'Online']
        places_future = ['Katowice', 'Bali', 'Online']
        for i in range(len(names_previous)):
            tournament = Tournament(
                name=names_previous[i],
                prize=randint(100000, 25000000),
                place=places_previous[i],
                start_date=timezone.now().date() - timedelta(days=randint(20, 50)),
                end_date=timezone.now().date() - timedelta(days=randint(1, 5)),
            )
            tournaments.append(tournament)
            print(tournament)

        for i in range(len(names_current)):
            tournament = Tournament(
                name=names_current[i],
                prize=randint(100000, 25000000),
                place=places_current[i],
                start_date=timezone.now().date() - timedelta(days=randint(3, 7)),
                end_date=timezone.now().date() + timedelta(days=randint(5, 10)),
            )
            tournaments.append(tournament)
            print(tournament)

        for i in range(len(names_future)):
            tournament = Tournament(
                name=names_future[i],
                prize=randint(100000, 25000000),
                place=places_future[i],
                start_date=timezone.now().date() + timedelta(days=randint(10, 15)),
                end_date=timezone.now().date() + timedelta(days=randint(35, 50)),
            )
            tournaments.append(tournament)
            print(tournament)
        Tournament.objects.bulk_create(tournaments)
        for tournament in tournaments:
            for team in teams:
                tournament.teams.add(team)
                tournament.save()
        print('\nall tournaments successfully created\n')

        # Creating tournament's stages
        print("Creating tournament's stages...\n")
        tournaments_stages = []
        stages = [
            TournamentStage.GROUP_STAGE,
            TournamentStage.ONE_EIGHT,
            TournamentStage.QUARTER_FINALS,
            TournamentStage.SEMI_FINALS,
            TournamentStage.FINAL,
        ]
        for tournament in tournaments:
            for i in range(5):
                tournaments_stage = TournamentStage(
                    stage=stages[i],
                    tournament=tournament,
                    start_date=tournament.start_date - timedelta(days=i),
                    end_date=tournament.end_date - timedelta(days=3),
                )
                print(tournaments_stage)
                tournaments_stages.append(tournaments_stage)
        TournamentStage.objects.bulk_create(tournaments_stages)
        print("\nall tournament's stages successfully created\n")

        # Creating matches and matches' periods
        print("Creating matches and matches' periods...\n")
        matches = []
        matches_periods = []
        formats = [BO1, BO3, BO5]
        for tournament in tournaments:
            participants = tournament.teams.all()
            if tournament.end_date < timezone.now().date():
                group_stage = tournament.tournament_stages.get(stage=TournamentStage.GROUP_STAGE)
                for i in range(len(participants)):
                    for j in range(i + 1, len(participants)):
                        create_match(group_stage, participants[i], participants[j], formats, matches, matches_periods)
                Match.objects.bulk_create(matches)
                MatchPeriod.objects.bulk_create(matches_periods)
                matches = []
                matches_periods = []

                one_eight = tournament.tournament_stages.get(stage=TournamentStage.ONE_EIGHT)
                create_matches(one_eight, formats, matches, matches_periods)
                Match.objects.bulk_create(matches)
                MatchPeriod.objects.bulk_create(matches_periods)
                matches = []
                matches_periods = []

                quarter_finals = tournament.tournament_stages.get(stage=TournamentStage.QUARTER_FINALS)
                create_matches(quarter_finals, formats, matches, matches_periods)
                Match.objects.bulk_create(matches)
                MatchPeriod.objects.bulk_create(matches_periods)
                matches = []
                matches_periods = []

                semi_finals = tournament.tournament_stages.get(stage=TournamentStage.SEMI_FINALS)
                create_matches(semi_finals, formats, matches, matches_periods)
                Match.objects.bulk_create(matches)
                MatchPeriod.objects.bulk_create(matches_periods)
                matches = []
                matches_periods = []

                final = tournament.tournament_stages.get(stage=TournamentStage.FINAL)
                teams = final.shuffle_teams()
                team1, team2 = teams[0]
                create_match(final, team1, team2, formats, matches, matches_periods)
                Match.objects.bulk_create(matches)
                MatchPeriod.objects.bulk_create(matches_periods)
                matches = []
                matches_periods = []

        print("\nall matches and matches' successfully created\n")

        print('DONE')

# Test queries

# 1) Кто выиграл хотя бы 400 матчей в своей карьере. >>> players = CareerPeriod.objects.values('player').annotate(
# summa=Sum('win_matches')).filter(summa__gt=400).values('player') >>> Player.objects.filter(id__in=players)
# <QuerySet [<Player: S1wH>, <Player: Miposhka>, <Player: Faith_Bian>]>

# 2) Игроки с именами не на букву A и А-русская
# >>> Player.objects.exclude(name__startswith='А')
# <QuerySet [<Player: S1wH>, <Player: Topson>, <Player: Miposhka>, <Player: Faith_Bian>, <Player: Yatoro>]>

# 3) Кто выиграл всех больше матчей
# >>> max_win_rate = CareerPeriod.objects.values('player').annotate(summa=Sum('win_matches')).aggregate(Max('summa'))
# >>> players = CareerPeriod.objects.values('player').annotate(summa=Sum('win_matches'))
# >>> players = players.filter(summa=max_win_rate['summa__max']).values('player')
# >>> Player.objects.filter(id__in=players)
# <QuerySet [<Player: Miposhka>]>

# 4) Карьеры игроков с nickname игрока на букву S которые играют в команде с названием в котором есть буква d
# CareerPeriod.objects.filter(player__nickname__startswith='S', team__name__contains='d') <QuerySet [<CareerPeriod:
# S1wH in team Liquid at period 2019-05-27 - 2020-04-16>, <CareerPeriod: S1wH in team Liquid at period 2020-04-16 -
# 2021-09-13>]>

# 5) Карьеры игроков у которых nickname и название команды начинаются на одну и ту же букву
