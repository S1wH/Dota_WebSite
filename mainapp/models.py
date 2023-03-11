# from django.db import models
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=32)
#     #avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.name}'
#
# # Create your models here.
# class News(models.Model):
#     title = models.CharField(max_length=32, unique=True)
#     summary = models.TextField()
#     # Основные типы полей
#     some_field = models.BooleanField(default=True)
#     # some_field = models.IntegerField
#     # some_field = models.FloatField
#     # some_field = models.DecimalField
#     # some_field = models.DateField
#     # some_field = models.TimeField
#     # some_field = models.DateTimeField
#     # some_field = models.BinaryField
#     # some_field = models.FileField
#     # some_field = models.ImageField
#     # some_field = models.EmailField
#     # some_field = models.URLField
#     # some_field = models.URLField
#
#     # Типы связей
#     # 1 - 1
#     # author = models.OneToOneField(Author)
#     # 1 - *
#     # on delete 1 - cascade
#     # 2 - protect
#     # 3 - set null
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     # * - *
#     # authors = models.ManyToManyField(Author)
#     class Meta:
#         verbose_name = 'News'
#         verbose_name_plural = 'News'
#
#     def __str__(self):
#         return f'{self.title}'
