from django.contrib import admin
from news.models import Author, News

# Register your models here.
admin.site.register(News)
admin.site.register(Author)