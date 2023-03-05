from django.db import models


class Author(models.Model):
    nickname = models.CharField(max_length=15)
    first_publish_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.nickname}'


class News(models.Model):
    header = models.CharField(max_length=30, unique=True)
    summary = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    publish_date = models.DateTimeField(auto_now_add=True)
    importance_index = models.BooleanField(default=False)
    # video = models.FileField(upload_to=)

    def __str__(self):
        return f'{self.header}'

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'