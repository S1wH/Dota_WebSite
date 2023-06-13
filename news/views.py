from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from news.models import News, Author
from .forms import NewsForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def get_news_info(request):
    return render(
        request,
        "news/news.html",
        context={
            "today_news": News.today_news(),
            "yesterday_news": News.yesterday_news(),
            "previous_news": News.previous_news(),
        },
    )


def get_one_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, "news/one_news.html", context={"news": news})


def create_author_view(request):
    # GET, - получение данных
    # заголовки, url - адрес
    # POST - изменение данных
    # заголовки, url - адрес, тело запроса
    if request.method == "GET":
        return render(request, "news/create_author.html", context={"is_error": False})
    else:
        # print(request)
        # print(request.POST)
        nickname = request.POST.get("nickname", "guest")
        rating = int(request.POST.get("rating", 0))
        if rating < 0 or rating > 5:
            return render(
                request,
                "news/create_author.html",
                context={
                    "is_error": True,
                    "error_text": "Рейтинг должен быть от 0 до 5",
                },
            )
        Author.objects.create(nickname=nickname, rating=rating)
        return HttpResponseRedirect("/admin/")


def create_news_view(request):
    if request.method == "POST":
        form = NewsForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/admin/")
    else:
        form = NewsForm()
    return render(request, "news/create_news.html", context={"form": form})


def update_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    if request.method == "POST":
        form = NewsForm(request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/admin/")
    else:
        form = NewsForm(instance=news)
    return render(request, "news/create_news.html", context={"form": form})


# 1.
# CRUD - Create Read Update Delete
# 5 list, detail


# Любой может смотреть список новостей
class NewsListView(ListView):
    model = News

    def get(self, request, *args, **kwargs):
        # print('REQUEST DATA: ', request.GET)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # return News.objects.filter(importance_index=True)
        return super().get_queryset().filter(importance_index=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["some text"] = "some text example"
        return context


# Только авторизованный может читать
class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News

    # get
    # get_context_data
    # get_queryset
    # get_object


# Админ
class NewsCreateView(UserPassesTestMixin, CreateView):
    model = News
    # fields = '__all__'
    form_class = NewsForm
    success_url = reverse_lazy("newsapp:news_list")

    def test_func(self):
        return self.request.user.is_superuser

    # get
    # get_context_data
    # get_form_kwargs
    # post
    # form_valid
    # form_invalid
    # get_success_url


# Править может сотрудник сайта
class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    # fields = '__all__'
    form_class = NewsForm
    success_url = reverse_lazy("newsapp:news_list")

    def test_func(self):
        user = self.request.user
        return user.is_staff and user.username == "user" and 1 == 1

    # get
    # get_context_data
    # get_form_kwargs
    # post
    # form_valid
    # form_invalid
    # get_success_url


class IsAdmin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Админ
class NewsDeleteView(IsAdmin, DeleteView):
    model = News
    success_url = reverse_lazy("newsapp:news_list")

    # get
    # get_context_data
    # post
    # get_success_url
