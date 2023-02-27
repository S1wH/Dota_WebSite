from django.shortcuts import render
from .models import News


def index_view(request):
    # some doing
    news = News.objects.all()
    videos = ['highlight.mp4', 'highlight.mp4', 'highlight.mp4', 'highlight.mp4']
    return render(request, 'mainapp/index.html', context={'news': news, 'videos': videos})