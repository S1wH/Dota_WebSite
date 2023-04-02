from django.http import HttpResponseRedirect
from django.shortcuts import render
from news.models import News, Author
from .forms import NewsForm
from datetime import datetime, timedelta


def get_news_info(request):
    return render(request, 'news/news.html', context={'today_news': News.today_news(),
                                                      'yesterday_news': News.yesterday_news(),
                                                      'previous_news': News.previous_news(),
                                                      })


def get_one_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/one_news.html', context={'news': news})


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


def update_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/create_news.html', context={'form': form})