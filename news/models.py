from django.db import models
from datetime import timedelta

from django.utils import timezone


class Author(models.Model):
    nickname = models.CharField(max_length=15)
    first_publish_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.nickname} with rating {self.rating}"


class News(models.Model):
    header = models.CharField(max_length=30, unique=True)
    summary = models.CharField(max_length=100)
    text = models.TextField()
    main_image = models.ImageField(upload_to="news_images", blank=True, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="author_news"
    )
    publish_date = models.DateTimeField(auto_now=True)
    importance_index = models.BooleanField(default=False)
    video = models.FileField(upload_to="news_videos", blank=True, null=True)

    @staticmethod
    def today_news():
        return News.objects.filter(publish_date__gte=timezone.now().date())

    @staticmethod
    def yesterday_news():
        return News.objects.filter(
            publish_date__lt=timezone.now().date(),
            publish_date__gte=timezone.now().date() - timedelta(days=1),
        )

    @staticmethod
    def previous_news():
        return News.objects.filter(
            publish_date__lte=timezone.now().date() - timedelta(days=2)
        )

    def images(self):
        return self.news_image.all()

    @staticmethod
    def important_news():
        news = News.objects.all().order_by("importance_index", "-publish_date")
        news = news[: len(news) - (len(news) % 4)]
        return [news[i : i + 4] for i in range(0, len(news), 4)]

    def __str__(self):
        return f"{self.id} {self.header}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Image(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="news_images")
    news_id = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name="news_image"
    )

    def __str__(self):
        return f"{self.title}"
