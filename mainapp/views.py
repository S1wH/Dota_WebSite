from django.shortcuts import render


def index_view(request):
    # some doing
    news = [
        {
            'title': 'Кто то выиграл интернешенл',
            'summary': 'Как круто это было',
        },
        {
            'title': '2222',
            'summary': '22222',
        },
        {
            'title': 'Кто то выиграл интернешенл',
            'summary': 'Как круто это было',
        },
    ]
    return render(request, 'mainapp/index.html', context={'news': news})