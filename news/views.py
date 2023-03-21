from django.http import HttpResponseRedirect
from django.shortcuts import render
from news.models import News, Author
from .forms import NewsForm
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


def create_author_view(request):
    # GET, - получение данных
    # заголовки, url - адрес
    # POST - изменение данных
    # заголовки, url - адрес, тело запроса
    if request.method == 'GET':
        return render(request, 'news/create_author.html', context={'is_error': False})
    else:
        print(request)
        print(request.POST)
        nickname = request.POST.get('nickname', 'guest')
        rating = int(request.POST.get('rating', 0))
        if rating < 0 or rating > 5:
            return render(request, 'news/create_author.html',
                          context={
                              'is_error': True,
                              'error_text': 'Рейтинг должен быть от 0 до 5'
                                   }
                          )
        Author.objects.create(nickname=nickname, rating=rating)
        return HttpResponseRedirect('/admin/')


def create_news_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', context={'form': form})