from django.shortcuts import render
from .models import News


def index_view(request):
    # some doing
    news = News.objects.all()
    return render(request, 'mainapp/index.html', context={'news': news})