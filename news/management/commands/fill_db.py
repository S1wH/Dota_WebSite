from django.core.management.base import BaseCommand, CommandError
from news.models import News, Author
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Fill db'

    def handle(self, *args, **options):
        # CRUD - Create Read Update Delete
        # Delete
        News.objects.all().delete()
        Author.objects.all().delete()

        # Create
        author = Author.objects.create(nickname='Andrey')
        author.nickname = 'Poll'
        author.save()

        # создание новости
        news = News.objects.create(
            header='test',
            summary='dfdf',
            text='dfdfdf',
            author=author
        )

        news = News.objects.create(
            header='uuiuiui',
            summary='1212',
            text='34343',
            author=author
        )

        # READ
        # all objects
        all_news = News.objects.all()

        # one object
        author = Author.objects.get(id=author.id)

        # filter
        authors = Author.objects.filter(nickname='Poll')
        # authors = Author.objects.filter(nickname='l')

        # get
        # 1
        # author = Author.objects.get(nickname='None')
        # print(author)
        Author.objects.create(nickname='Leo')

        authors = Author.objects.filter(rating=0)

        # authors = Author.objects.get(rating=0)
        # print(authors)

        # author = Author.objects.get(nickname='None')
        # print(author)

        # EXCLUDE
        # рейтинг не равен 0
        authors = Author.objects.exclude(rating=0)
        print(authors)

        # зовут не Leo рейтинг 0
        authors = Author.objects.exclude(nickname='Leo').filter(rating=0)
        print(authors)

        # LOOKUPS
        # рейтинг больше 0
        authors = Author.objects.filter(rating__gt=0)
        authors = Author.objects.filter(rating__gte=0)
        authors = Author.objects.filter(rating__lt=0)
        authors = Author.objects.filter(rating__lte=0, nickname='Leo')
        print(authors)

        # имя начинается с буквы P
        authors = Author.objects.filter(nickname__startswith='P')
        print(authors)

        # RELATION MODEL
        # связанная модель
        # Найти новости автора у которого имя Poll
        # 1.
        author = Author.objects.get(nickname='Poll')
        news = News.objects.filter(author=author)
        print(news)

        # 2.
        news = News.objects.filter(author__nickname='Poll')
        print(news)
        # Найти новости автора у которого имя начинается на P
        news = News.objects.filter(author__nickname__startswith='P')
        print(news)

        # RELATED_NAME

        one_news = news.first()
        print(one_news)

        print(author)

        # Из новости автор
        print(one_news.author)

        # Наоборот есть автор, надо взять его новости
        # 1. запросом
        print(News.objects.filter(author=author))

        # 2. related_name
        print(author.author_news.all())
        print(author.news_set.all())



        print('DONE')

        # - Кто выиграл хотя бы 100 матч в своей карьере
        # >>> News.objects.all()
        # <QuerySet [<News: test>, <News: uuiuiui>]>