from django.shortcuts import render
from .models import News

# Create your views here.

def set_news_info(request):
    all_news = [
        [
            {'description': 'First',
             'date': '24.02.2023'},
            {'description': 'Second',
             'date': '24.02.2023'},
            {'description': 'Third',
             'date': '24.02.2023'},
            {'description': 'Forth',
             'date': '24.02.2023'},
            {'description': 'Fifth',
             'date': '24.02.2023'},
            {'description': 'Sixth',
             'date': '24.02.2023'},
        ],
        [
            {'description': 'First',
             'date': '23.02.2023'},
            {'description': 'Second',
             'date': '23.02.2023'},
            {'description': 'Third',
             'date': '23.02.2023'},
            {'description': 'Forth',
             'date': '23.02.2023'},
            {'description': 'Fifth',
             'date': '23.02.2023'},
            {'description': 'Sixth',
             'date': '23.02.2023'},
        ],
        [
            {'description': 'First',
             'date': '18.02.2023'},
            {'description': 'Second',
             'date': '16.02.2023'},
            {'description': 'Third',
             'date': '13.02.2023'},
            {'description': 'Forth',
             'date': '10.02.2023'},
            {'description': 'Fifth',
             'date': '05.02.2023'},
            {'description': 'Sixth',
             'date': '01.02.2023'},
        ],
    ]
    return render(request, 'news/news.html', context={'all_news': all_news})


def get_one_news_view(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/one_news.html', context={'news': news})