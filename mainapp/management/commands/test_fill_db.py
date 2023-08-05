from random import choice, randint
from datetime import timedelta
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.images import ImageFile
from django.conf import settings
from news.models import News, Author, Image
from teams_and_players.models import Team, Player, CareerPeriod
from tournaments.models import Tournament, TournamentStage
from matches.models import Match, MatchPeriod, BO1, BO3, BO5, PLAYED

FORMATS = [BO1, BO3, BO5]
COUNTRIES = ["Russia", "US", "Germany", "Brazil", "Spain", "UK"]

PLAYERS = []
TEAMS = []
TOURNAMENTS = []
NEWS = []
AUTHORS = []
MATCHES = []
MATCH_PERIODS = []


def create_authors():
    author_nicknames = [
        "Paul",
        "Andrew",
        "Nikolai",
        "Gleb",
        "Slava",
    ]
    for i in range(len(author_nicknames)):
        author = Author(nickname=author_nicknames[i], rating=i + 1)
        AUTHORS.append(author)
        print(author)
    Author.objects.bulk_create(AUTHORS)


def create_news():
    for i in range(11):
        one_news = News.objects.create(
            header=f"News №{i + 1}",
            summary=f"This is a brief summary of a news with a header News №{i + 1}",
            text=f"Here should be a really long text about news with a header News №{i + 1},"
            f" but I am kinda lazy.\n"
            "Although this text makes sense. I am glad to write it,"
            " because I do it instead of listening "
            "to my Physics teacher",
            author=choice(AUTHORS),
            publish_date=timezone.now(),
            importance_index=i < 9,
        )
        path = os.path.join(settings.BASE_DIR, f"static/photos/dota/news{i + 1}.jpg")
        with open(path, "rb") as file:
            one_news.main_image = ImageFile(file, name=f"news{i + 1}.jpg")
            one_news.save()
            print(one_news, one_news.publish_date)
            NEWS.append(one_news)


def create_images():
    for item in NEWS:
        for i in range(3):
            with open("one_news.jpg", "rb") as file:
                image = Image.objects.create(
                    title=f"title {i} for {item}",
                    image=ImageFile(file),
                    news_id=item,
                )
                print(image)


def create_teams():
    teams_names = [
        "team Spirit",
        "team Liquid",
        "PSG.LGD",
        "team Secret",
        "Na'Vi",
        "BetBoom",
        "Nemiga",
        "One Move",
        "VP",
        "Entity",
        "OG",
        "Evil Geniuses",
        "Gladiators",
        "Thunder",
        "BOOM",
        "Aster",
    ]

    for i in range(16):
        team = Team.objects.create(
            name=teams_names[i],
            country=choice(COUNTRIES),
            establish_date="2003-12-23",
            biography=f"{teams_names[i]} is a really great team. "
            f"It was performing wonderfully",
            prize=randint(1000000, 15000000),
            win_matches=randint(1000, 2000),
            lose_matches=randint(500, 1200),
            draw_matches=randint(10, 100),
        )
        path = os.path.join(settings.BASE_DIR, f"static/photos/team{i + 1}.jpg")
        with open(path, "rb") as file:
            team.logo = ImageFile(file, name=f"team{i + 1}.jpg")
            team.save()
            print(team)
            TEAMS.append(team)


def create_players():
    names = [
        "Paul",
        "Topias",
        "Kirill",
        "Chua",
        "Oleg",
    ]
    nicknames = [
        "S1wH",
        "Topson",
        "Miposhka",
        "Faith_Bian",
        "Yatoro",
    ]
    for i in range(5):
        player = Player.objects.create(
            name=names[i],
            nickname=nicknames[i],
            age=randint(18, 30),
            birthday="2003-12-23",
            country=choice(COUNTRIES),
            biography="This player is great. I am serious."
            "He won a lot of trophies and made all his "
            "teams great once again.",
        )
        path = os.path.join(settings.BASE_DIR, "static/photos/player.jpg")
        with open(path, "rb") as file:
            player.photo = ImageFile(file, name=f"player{i + 1}.jpg")
            player.save()
            print(player)
            PLAYERS.append(player)


def create_career_histories():
    roles = ["support", "carry", "semi-support", "off-lane", "mid-lane"]
    dates = ["2017-12-23", "2019-05-27", "2020-04-16", "2021-09-13", None]
    periods = []

    for player in PLAYERS:
        for i in range(4):
            period = CareerPeriod(
                player=player,
                team=choice(TEAMS),
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


def create_tournaments():
    names_previous = [
        "ESL COLOGNE 2023",
        "Paris Major 2023",
        "DPC League season 13",
    ]
    names_current = [
        "ESL Antwerpen 2023",
        "Moscow Major 2023",
        "DPC League season 14",
    ]
    names_future = ["ESL Katowice 2023", "Bali Major 2023", "DPC League season 15"]
    places_previous = ["Cologne", "Paris", "Online"]
    places_current = ["Antwerpen", "Moscow", "Online"]
    places_future = ["Katowice", "Bali", "Online"]
    for i in range(len(names_previous)):
        tournament = Tournament(
            name=names_previous[i],
            prize=randint(100000, 25000000),
            place=places_previous[i],
            start_date=timezone.now().date() - timedelta(days=randint(20, 50)),
            end_date=timezone.now().date() - timedelta(days=randint(1, 5)),
        )
        TOURNAMENTS.append(tournament)
        print(tournament)

    for i in range(len(names_current)):
        tournament = Tournament(
            name=names_current[i],
            prize=randint(100000, 25000000),
            place=places_current[i],
            start_date=timezone.now().date() - timedelta(days=randint(3, 7)),
            end_date=timezone.now().date() + timedelta(days=randint(5, 10)),
        )
        TOURNAMENTS.append(tournament)
        print(tournament)

    for i in range(len(names_future)):
        tournament = Tournament(
            name=names_future[i],
            prize=randint(100000, 25000000),
            place=places_future[i],
            start_date=timezone.now().date() + timedelta(days=randint(10, 15)),
            end_date=timezone.now().date() + timedelta(days=randint(35, 50)),
        )
        TOURNAMENTS.append(tournament)
        print(tournament)

    Tournament.objects.bulk_create(TOURNAMENTS)
    for tournament in TOURNAMENTS:
        for team in TEAMS:
            tournament.teams.add(team)
        tournament.save()


def create_stages():
    tournaments_stages = []
    stages = [
        TournamentStage.GROUP_STAGE,
        TournamentStage.ONE_EIGHT,
        TournamentStage.QUARTER_FINALS,
        TournamentStage.SEMI_FINALS,
        TournamentStage.FINAL,
    ]
    for tournament in TOURNAMENTS:
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


def create_match(stage, team1, team2):
    match = Match(
        start_date=stage.start_date,
        end_date=stage.start_date + timedelta(minutes=40),
        team1=team1,
        team2=team2,
        status=PLAYED,
        tournament_stage=stage,
        format=choice(FORMATS),
    )
    amount_periods = 0
    while amount_periods < int(match.format):
        match_period = MatchPeriod(
            win_team=choice([match.team1, match.team2]),
            duration=timedelta(minutes=45),
            match=match,
        )
        MATCH_PERIODS.append(match_period)
        amount_periods += 1
    MATCHES.append(match)
    print(match)


def get_winners_and_losers():
    for match in MATCHES:
        match.match_winner()
        match.match_loser()
        match.save()


def create_stage_matches(stage):
    teams = stage.shuffle_teams()
    for pair in teams:
        team1, team2 = pair
        create_match(stage, team1, team2)


def clear_matches():
    MATCHES.clear()
    MATCH_PERIODS.clear()


def create_all_matches():
    for tournament in TOURNAMENTS:
        participants = tournament.teams.all()
        if tournament.end_date < timezone.now().date():
            group_stage = tournament.tournament_stages.get(
                stage=TournamentStage.GROUP_STAGE
            )
            for team in participants:
                group_stage.teams.add(team)
            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    create_match(
                        group_stage,
                        participants[i],
                        participants[j],
                    )
            Match.objects.bulk_create(MATCHES)
            MatchPeriod.objects.bulk_create(MATCH_PERIODS)
            get_winners_and_losers()
            Match.objects.bulk_update(MATCHES, ["winner", "loser"])
            group_stage.group_stage_table()
            clear_matches()

            one_eight = tournament.tournament_stages.get(
                stage=TournamentStage.ONE_EIGHT
            )
            create_stage_matches(one_eight)
            Match.objects.bulk_create(MATCHES)
            MatchPeriod.objects.bulk_create(MATCH_PERIODS)
            get_winners_and_losers()
            Match.objects.bulk_update(MATCHES, ["winner", "loser"])
            one_eight.stage_winners()
            clear_matches()

            quarter_finals = tournament.tournament_stages.get(
                stage=TournamentStage.QUARTER_FINALS
            )
            create_stage_matches(quarter_finals)
            Match.objects.bulk_create(MATCHES)
            MatchPeriod.objects.bulk_create(MATCH_PERIODS)
            get_winners_and_losers()
            Match.objects.bulk_update(MATCHES, ["winner", "loser"])
            quarter_finals.stage_winners()
            clear_matches()

            semi_finals = tournament.tournament_stages.get(
                stage=TournamentStage.SEMI_FINALS
            )
            create_stage_matches(semi_finals)
            Match.objects.bulk_create(MATCHES)
            MatchPeriod.objects.bulk_create(MATCH_PERIODS)
            get_winners_and_losers()
            Match.objects.bulk_update(MATCHES, ["winner", "loser"])
            semi_finals.stage_winners()
            clear_matches()

            final = tournament.tournament_stages.get(stage=TournamentStage.FINAL)
            teams = final.shuffle_teams()
            team1, team2 = teams[0]
            create_match(final, team1, team2)
            Match.objects.bulk_create(MATCHES)
            MatchPeriod.objects.bulk_create(MATCH_PERIODS)
            get_winners_and_losers()
            Match.objects.bulk_update(MATCHES, ["winner", "loser"])
            final.stage_winners()
            clear_matches()


class Command(BaseCommand):
    help = "Filling database with test data"

    def handle(self, *args, **kwargs):
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
        print("Creating authors...\n")
        create_authors()
        print("\nall authors successfully created\n")

        # Creating news
        print("Creating news...\n")
        create_news()
        print("\nAll news successfully created\n")

        # Creating Images for news
        print("Creating images for news...\n")
        create_images()
        print("\nAll images successfully created\n")

        # Creating teams
        print("Creating teams...\n")
        create_teams()
        print("\nAll teams successfully created\n")

        # Creating players
        print("Creating players...\n")
        create_players()
        print("\nall players successfully created\n")

        # Creating Career Histories
        print("Creating career periods...\n")
        create_career_histories()
        print("\nall career periods successfully created\n")

        # Creating Tournaments
        print("Creating tournaments...\n")
        create_tournaments()
        print("\nall tournaments successfully created\n")

        # Creating tournament's stages
        print("Creating tournament's stages...\n")
        create_stages()
        print("\nall tournament's stages successfully created\n")

        # Creating matches and matches' periods
        print("Creating matches and matches' periods...\n")
        create_all_matches()
        print("\nall matches and matches' successfully created\n")

        print("DONE")
