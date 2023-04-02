from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from news.models import News, Author, Image
from teams_and_players.models import Team, Player, CareerPeriod
from django.core.files.images import ImageFile
from random import choice, randint
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Filling database with test data'

    def handle(self, *args, **options):
        # Delete all previous data
        Author.objects.all().delete()
        News.objects.all().delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        CareerPeriod.objects.all().delete()

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
            author = Author.objects.create(
                nickname=author_nicknames[i],
                rating=i + 1
            )
            authors.append(author)
            print(author)
        print('\nall authors successfully created\n')

        # Creating news
        print('Creating news...\n')
        news = []
        for i in range(11):
            one_news = News.objects.create(
                header=f'News №{i + 1}',
                summary=f'This is a brief summary of a news with a header News №{i + 1}',
                text=f'Here should be a really long text about news with a header News №{i + 1}, but I am kinda lazy.\n'
                     'Although this text makes sense. I am glad to write it, because I do it instead of listening '
                     'to my Physics teacher',
                author=choice(authors),
                publish_date=datetime.now(),
                importance_index=True if i < 9 else False,
            )
            path = os.path.join(settings.BASE_DIR, f'static/photos/dota/news{i + 1}.jpg')
            one_news.main_image = ImageFile(open(path, 'rb'), name=f'one_news{i + 1}.jpg')
            if 4 < i < 8:
                one_news.publish_date = datetime.now().date() - timedelta(days=1)
            elif i > 8:
                one_news.publish_date = datetime.now().date() - timedelta(days=5)
            one_news.save()
            print(one_news, one_news.publish_date)
            news.append(one_news)
        print('\nAll news successfully created\n')

        # Creating Images for news
        print('Creating images for news...\n')
        for item in news:
            for i in range(3):
                image = Image.objects.create(
                    title=f'title {i} for {item}',
                    image=ImageFile(open(f'one_news.jpg', 'rb')),
                    news_id=item,
                )
                print(image)
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
        ]
        countries = ['Russia', 'US', 'Germany']

        for i in range(5):
            team = Team.objects.create(
                name=teams_names[i],
                country=choice(countries),
                establish_date='2003-12-23',
                biography=f'{teams_names[i]} is a really great team. '
                          f'It was performing wonderfully',
                all_prize=randint(1000000, 15000000),
                win_matches=randint(1000, 2000),
                lose_matches=randint(500, 1200),
                draw_matches=randint(10, 100),
            )
            path = os.path.join(settings.BASE_DIR, f'static/photos/team{i + 1}.jpg')
            team.logo = ImageFile(open(path, 'rb'), name=f'team{i + 1}.jpg')
            team.save()
            print(team)
            teams.append(team)

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
            player = Player.objects.create(
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
            player.save()
            print(player)
            players.append(player)
        print('\nall players successfully created\n')

        # Creating Career Histories
        print('Creating career periods...\n')
        roles = ['support', 'carry', 'semi-support', 'off-lane', 'mid-lane']
        dates = ['2017-12-23', '2019-05-27', '2020-04-16', '2021-09-13', None]
        periods = []

        for player in players:
            one_player_periods = []
            for i in range(4):
                period = CareerPeriod.objects.create(
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
                one_player_periods.append(period)
                print(period)
            periods.append(one_player_periods)
        print('\nall career periods successfully created\n')
        print('DONE')

# Test queries

# 1) Кто выиграл хотя бы 400 матчей в своей карьере.
# >>> players = CareerPeriod.objects.values('player').annotate(summa=Sum('win_matches')).filter(summa__gt=400).values('player')
# >>> Player.objects.filter(id__in=players)
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
# CareerPeriod.objects.filter(player__nickname__startswith='S', team__name__contains='d')
# <QuerySet [<CareerPeriod: S1wH in team Liquid at period 2019-05-27 - 2020-04-16>, <CareerPeriod: S1wH in team Liquid at period 2020-04-16 - 2021-09-13>]>

# 5) Карьеры игроков у которых nickname и название команды начинаются на одну и ту же букву
