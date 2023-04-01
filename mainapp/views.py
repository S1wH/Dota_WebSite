from django.shortcuts import render
from news.models import News


def index_view(request):
    videos = ['highlight.mp4', 'highlight.mp4', 'highlight.mp4', 'highlight.mp4']
    return render(request, 'mainapp/index.html', context={'main_news': News.important_news(), 'videos': videos})
