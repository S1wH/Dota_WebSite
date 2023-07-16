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
from django.urls import path, include, re_path
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    path('api-token-auth/', obtain_auth_token),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth-jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth-jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth-jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
   openapi.Info(
      title="My Dota API",
      default_version='v1',
      description="API TO MY DOTA description",
      terms_of_service="https://github.com/S1wH/Dota_WebSite",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="None"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$',
           schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
           name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
