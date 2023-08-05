from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tournaments import views
from tournaments.api.views import TournamentViewSet, TournamentStageViewSet

router = DefaultRouter()
router.register("tournaments", TournamentViewSet)
router.register("tournament_stages", TournamentStageViewSet)

app_name = "tournaments_app"

urlpatterns = [
    path(
        "current_tournaments/",
        views.TournamentsCurrentListView.as_view(),
        name="tournaments_current_list",
    ),
    path(
        "previous_tournaments/",
        views.TournamentsPreviousListView.as_view(),
        name="tournaments_previous_list",
    ),
    path(
        "future_tournaments/",
        views.TournamentsFutureListView.as_view(),
        name="tournaments_future_list",
    ),
    path("<int:pk>/", views.TournamentDetailView.as_view(), name="one_tournament"),
    # api views
    path('api/', include(router.urls)),
]
