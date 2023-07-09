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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from matches import views
from matches.api.views import MatchViewSet, MatchPeriodViewSet

router = DefaultRouter()
router.register("matches", MatchViewSet)
router.register("match_periods", MatchPeriodViewSet)

app_name = "matchesapp"

urlpatterns = [
    path(
        "ongoing_matches/",
        views.MatchesOngoingListView.as_view(),
        name="matches_ongoing_list",
    ),
    path(
        "incoming_matches/",
        views.MatchesIncomingListView.as_view(),
        name="matches_incoming_list",
    ),
    path(
        "played_matches/",
        views.MatchesPlayedListView.as_view(),
        name="matches_played_list",
    ),
    # api views
    path("api/", include(router.urls)),
]
