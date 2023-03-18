from django.shortcuts import render
from news.models import News
from _datetime import datetime, timedelta


def get_news_info(request):
    all_today_news = News.objects.filter(publish_date__gte=datetime.now().date())
    all_yesterday_news = News.objects.filter(publish_date__gte=datetime.now().date() - timedelta(days=1),
                                             publish_date__lt=datetime.now().date())
    all_previous_news = News.objects.filter(publish_date__lt=datetime.now().date() - timedelta(days=1))
    return render(request, 'news/news.html', context={'all_today_news': all_today_news,
                                                      'all_yesterday_news': all_yesterday_news,
                                                      'all_previous_news': all_previous_news,
                                                      })


def get_one_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    images = news.news_image.all()
    return render(request, 'news/one_news.html', context={'news': news, 'images': images,})
