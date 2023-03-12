from django.shortcuts import render
from news.models import News


def index_view(request):
    news = News.objects.all().order_by('importance_index', '-publish_date')
    # important_news = sorted([item for item in news if item.importance_index is True], key=lambda item: item.publish_date
    #                         , reverse=True)
    # important_news = important_news[:len(important_news) - (len(important_news) % 4)]
    # important_news = [important_news[i:i + 4] for i in range(0, len(important_news), 4)]
    # print(important_news)
    # for item in important_news:
    #     print(item.publish_date)
    videos = ['highlight.mp4', 'highlight.mp4', 'highlight.mp4', 'highlight.mp4']
    return render(request, 'mainapp/index.html', context={'main_news': news, 'videos': videos})
