from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from news.models import News

def is_superuser(user):
    return user.is_superuser

def is_admin(view):
    @user_passes_test(is_superuser)
    def inner(*args, **kwargs):
        return view(*args, **kwargs)

    return inner

# @login_required
@is_admin
def index_view(request):
    videos = ['highlight.mp4', 'highlight.mp4', 'highlight.mp4', 'highlight.mp4']
    return render(request, 'mainapp/index.html', context={'main_news': News.important_news(), 'videos': videos})


@user_passes_test(is_superuser)
def other(request):
    videos = ['highlight.mp4', 'highlight.mp4', 'highlight.mp4', 'highlight.mp4']
    return render(request, 'mainapp/index.html', context={'main_news': News.important_news(), 'videos': videos})