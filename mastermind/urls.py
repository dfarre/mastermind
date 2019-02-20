from django import urls

from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from mastermind import views


router = routers.SimpleRouter()

router.register('games', views.GameViewSet)
router.register('boards', views.BoardViewSet)
router.register('guesses', views.GuessViewSet)

urlpatterns = [
    urls.path('', urls.include('rest_framework.urls')),
    urls.path('token-auth/', authtoken_views.obtain_auth_token),
    urls.path('', urls.include(router.urls)),
]
