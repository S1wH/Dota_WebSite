from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from news.models import News, Author
from .forms import NewsForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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


# 1.
# CRUD - Create Read Update Delete
# 5 list, detail

# Любой может смотреть список новостей
class NewsListView(ListView):
    model = News


# Только авторизованный может читать
class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News


# Админ
class NewsCreateView(UserPassesTestMixin, CreateView):
    model = News
    # fields = '__all__'
    form_class = NewsForm
    success_url = reverse_lazy('newsapp:news_list')

    def test_func(self):
        return self.request.user.is_superuser


# Править может сотрудник сайта
class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    # fields = '__all__'
    form_class = NewsForm
    success_url = reverse_lazy('newsapp:news_list')

    def test_func(self):
        user = self.request.user
        return user.is_staff and user.username == 'user' and 1 == 1


class IsAdmin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


# Админ
class NewsDeleteView(IsAdmin, DeleteView):
    model = News
    success_url = reverse_lazy('newsapp:news_list')
