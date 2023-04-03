"""my_dota URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from news import views

app_name = 'newsapp'

urlpatterns = [
    path('', views.get_news_info, name='index'),
    path('<int:news_id>/', views.get_one_news_view, name='one_news'),
    path('author/create/', views.create_author_view, name='create_author'),
    path('news/create/', views.create_news_view, name='create_news'),
    path('news/update/<int:news_id>/', views.update_news_view, name='update_news'),
    # CBV
    path('list/', views.NewsListView.as_view(), name='news_list'),
    path('detail/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('update/<int:pk>/', views.NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
]
