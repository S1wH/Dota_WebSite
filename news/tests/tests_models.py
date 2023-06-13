from django.test import TestCase
from mixer.backend.django import mixer
from news.models import Author, News, Image


class TestAuthor(TestCase):
    def test_str(self):
        author = Author.objects.create(nickname="Pishkin", rating=1)
        self.assertEqual(str(author), "Pishkin with rating 1")


# def mock_timezone():
#     return '21/02/2222'


class TestNews(TestCase):
    def test_today_news(self):
        news1 = mixer.blend(News)
        news2 = mixer.blend(News)
        # timezone.now() => '21/02/2222'
        # timezone = mock_timezone
        self.assertEqual(list(News.today_news()), [news1, news2])

    # def test_yesterday_news(self):
    #     news1 = mixer.blend(News)
    #     news2 = mixer.blend(News)
    #     self.assertEqual([news for news in News.yesterday_news()], [news1, news2])
    #
    # def test_previous_news(self):

    #     news1 = mixer.blend(News, publish_date=datetime.now().date() - timedelta(days=3))
    #     news2 = mixer.blend(News, publish_date=datetime.now().date() - timedelta(days=10))
    #     self.assertEqual([news for news in News.previous_news()], [news1, news2])

    def test_images(self):
        news = mixer.blend(News)
        image1 = mixer.blend(Image, news_id=news)
        image2 = mixer.blend(Image, news_id=news)
        self.assertEqual(list(News.images(news)), [image1, image2])
