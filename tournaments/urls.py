from django.urls import path
from tournaments import views

app_name = 'tournaments_app'

urlpatterns = [
    path('current_tournaments/', views.TournamentsCurrentListView.as_view(), name='tournaments_current_list'),
    path('previous_tournaments/', views.TournamentsPreviousListView.as_view(), name='tournaments_previous_list'),
    path('future_tournaments/', views.TournamentsFutureListView.as_view(), name='tournaments_future_list'),
    path('<int:pk>/', views.TournamentDetailView.as_view(), name='one_tournament'),
]
