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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token

# DRF
from users.models import MyUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ["url", "username", "email", "is_staff"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mainapp.urls")),
    path("news/", include("news.urls")),
    path("teams_and_players/", include("teams_and_players.urls")),
    path("matches/", include("matches.urls")),
    path("users/", include("users.urls")),
    path("matches/", include("matches.urls")),
    path("tournaments/", include("tournaments.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path('api-token-auth/', obtain_auth_token)
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
